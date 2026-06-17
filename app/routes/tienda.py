from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.tienda import Producto, CarritoItem, Compra, CompraItem

tienda = Blueprint('tienda', __name__)


# ─── CATÁLOGO ────────────────────────────────────────────────────────────────

@tienda.route('/tienda')
@login_required
def catalogo():
    categoria = request.args.get('categoria', '')
    if categoria:
        productos = Producto.query.filter_by(activo=True, categoria=categoria).all()
    else:
        productos = Producto.query.filter_by(activo=True).all()

    categorias = db.session.query(Producto.categoria).filter(
        Producto.activo == True, Producto.categoria != None
    ).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]

    return render_template('tienda/catalogo.html',
                           productos=productos,
                           categorias=categorias,
                           categoria_activa=categoria)


# ─── CARRITO ─────────────────────────────────────────────────────────────────

@tienda.route('/tienda/carrito')
@login_required
def carrito():
    items = CarritoItem.query.filter_by(usuario_id=current_user.id).all()
    total = sum(i.subtotal() for i in items)
    return render_template('tienda/carrito.html', items=items, total=total)


@tienda.route('/tienda/agregar/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad', 1))

    if cantidad < 1 or cantidad > producto.stock:
        flash('Cantidad no válida.', 'danger')
        return redirect(url_for('tienda.catalogo'))

    item = CarritoItem.query.filter_by(
        usuario_id=current_user.id, producto_id=producto_id
    ).first()

    if item:
        nueva_cantidad = item.cantidad + cantidad
        if nueva_cantidad > producto.stock:
            flash('No hay suficiente stock disponible.', 'danger')
            return redirect(url_for('tienda.catalogo'))
        item.cantidad = nueva_cantidad
    else:
        item = CarritoItem(
            usuario_id=current_user.id,
            producto_id=producto_id,
            cantidad=cantidad
        )
        db.session.add(item)

    db.session.commit()
    flash(f'"{producto.nombre}" agregado al carrito.', 'success')
    return redirect(url_for('tienda.catalogo'))


@tienda.route('/tienda/carrito/eliminar/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    item = CarritoItem.query.get_or_404(item_id)
    if item.usuario_id != current_user.id:
        flash('Acción no permitida.', 'danger')
        return redirect(url_for('tienda.carrito'))
    db.session.delete(item)
    db.session.commit()
    flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('tienda.carrito'))


@tienda.route('/tienda/carrito/actualizar/<int:item_id>', methods=['POST'])
@login_required
def actualizar_cantidad(item_id):
    item = CarritoItem.query.get_or_404(item_id)
    if item.usuario_id != current_user.id:
        flash('Acción no permitida.', 'danger')
        return redirect(url_for('tienda.carrito'))

    cantidad = int(request.form.get('cantidad', 1))
    if cantidad < 1:
        db.session.delete(item)
    elif cantidad > item.producto.stock:
        flash('No hay suficiente stock.', 'danger')
        return redirect(url_for('tienda.carrito'))
    else:
        item.cantidad = cantidad

    db.session.commit()
    return redirect(url_for('tienda.carrito'))


# ─── CONFIRMAR COMPRA ─────────────────────────────────────────────────────────

@tienda.route('/tienda/confirmar')
@login_required
def confirmar_compra():
    items = CarritoItem.query.filter_by(usuario_id=current_user.id).all()
    if not items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('tienda.catalogo'))
    total = sum(i.subtotal() for i in items)
    return render_template('tienda/confirmar.html', items=items, total=total)


@tienda.route('/tienda/finalizar', methods=['POST'])
@login_required
def finalizar_compra():
    items = CarritoItem.query.filter_by(usuario_id=current_user.id).all()
    if not items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('tienda.catalogo'))

    # Validar stock antes de confirmar
    for item in items:
        if item.cantidad > item.producto.stock:
            flash(f'Sin stock suficiente para "{item.producto.nombre}".', 'danger')
            return redirect(url_for('tienda.carrito'))

    total = sum(i.subtotal() for i in items)

    compra = Compra(usuario_id=current_user.id, total=total)
    db.session.add(compra)
    db.session.flush()  # para obtener compra.id

    for item in items:
        compra_item = CompraItem(
            compra_id=compra.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        db.session.add(compra_item)
        # Descontar stock
        item.producto.stock -= item.cantidad
        db.session.delete(item)

    db.session.commit()
    flash('¡Compra realizada con éxito!', 'success')
    return redirect(url_for('tienda.compra_exitosa', compra_id=compra.id))


@tienda.route('/tienda/compra-exitosa/<int:compra_id>')
@login_required
def compra_exitosa(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    if compra.usuario_id != current_user.id:
        flash('Acción no permitida.', 'danger')
        return redirect(url_for('tienda.catalogo'))
    return render_template('tienda/compra_exitosa.html', compra=compra)



# ─── RESERVAR (modal → carrito) ──────────────────────────────────────────────

@tienda.route('/tienda/reservar/<int:producto_id>', methods=['POST'])
@login_required
def reservar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad', 1))

    if cantidad < 1 or cantidad > producto.stock:
        flash('Cantidad no válida.', 'danger')
        return redirect(url_for('tienda.catalogo'))

    item = CarritoItem.query.filter_by(
        usuario_id=current_user.id, producto_id=producto_id
    ).first()

    if item:
        nueva_cantidad = item.cantidad + cantidad
        if nueva_cantidad > producto.stock:
            flash('No hay suficiente stock disponible.', 'danger')
            return redirect(url_for('tienda.catalogo'))
        item.cantidad = nueva_cantidad
    else:
        item = CarritoItem(
            usuario_id=current_user.id,
            producto_id=producto_id,
            cantidad=cantidad
        )
        db.session.add(item)

    db.session.commit()
    flash(f'"{producto.nombre}" agregado al carrito.', 'success')
    return redirect(url_for('tienda.carrito'))


# ─── HISTORIAL DE COMPRAS ─────────────────────────────────────────────────────

@tienda.route('/tienda/historial')
@login_required
def historial_compras():
    compras = Compra.query.filter_by(usuario_id=current_user.id)\
                         .order_by(Compra.fecha.desc()).all()
    return render_template('tienda/historial_compras.html', compras=compras)


# ─── ADMIN: GESTIÓN DE PRODUCTOS ─────────────────────────────────────────────

@tienda.route('/admin/productos')
@login_required
def admin_productos():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))

    busqueda = request.args.get('busqueda', '').strip()
    categoria = request.args.get('categoria', '')

    query = Producto.query
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))
    if categoria:
        query = query.filter(Producto.categoria == categoria)

    productos = query.all()

    categorias = db.session.query(Producto.categoria).filter(
        Producto.categoria != None
    ).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]

    return render_template('tienda/admin_productos.html',
                           productos=productos,
                           categorias=categorias,
                           busqueda=busqueda,
                           categoria_activa=categoria)


@tienda.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio', 0))
        stock = int(request.form.get('stock', 0))
        categoria = request.form.get('categoria')

        imagen_url = request.form.get('imagen_url', '').strip() or None
        imagen_ancho = int(request.form.get('imagen_ancho', 300))
        imagen_alto  = int(request.form.get('imagen_alto',  200))
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            imagen_url=imagen_url,
            imagen_ancho=imagen_ancho,
            imagen_alto=imagen_alto
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('tienda.admin_productos'))

    return render_template('tienda/form_producto.html', producto=None)


@tienda.route('/admin/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))

    producto = Producto.query.get_or_404(producto_id)

    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = float(request.form.get('precio', 0))
        producto.stock = int(request.form.get('stock', 0))
        producto.categoria = request.form.get('categoria')
        producto.imagen_url = request.form.get('imagen_url', '').strip() or None
        producto.imagen_ancho = int(request.form.get('imagen_ancho', 300))
        producto.imagen_alto  = int(request.form.get('imagen_alto',  200))
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('tienda.admin_productos'))

    return render_template('tienda/form_producto.html', producto=producto)


@tienda.route('/admin/productos/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    if current_user.rol != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))

    producto = Producto.query.get_or_404(producto_id)
    producto.activo = False  # baja lógica
    db.session.commit()
    flash('Producto dado de baja.', 'info')
    return redirect(url_for('tienda.admin_productos'))
