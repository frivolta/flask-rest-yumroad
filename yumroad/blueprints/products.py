from flask import Blueprint, render_template
from yumroad.models import Product

products = Blueprint('products', __name__)


@products.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/details.html', product=product)


@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404
