{
    'name': 'Sale Multi Delivery Address',
    'version': '16.0',
    'summary': """Set delivery address per sale order line and split DOs accordingly.""",
    'description': """
This module allows assigning different delivery addresses per sale order line and splits delivery orders accordingly.

✔ Line-wise Delivery Address — Set unique delivery address for each order line  
✔ Auto Split Delivery Orders — Creates separate DOs based on delivery addresses  
✔ Enhanced Logistics Control — Better planning for multi-location shipments  
✔ Accurate DO Reports — Shows respective addresses in delivery PDF  
✔ Sale Order Report Update — Reflects custom address on quotation PDF  
✔ Seamless Workflow Integration — Works with existing sale and stock apps  

Ideal for companies dispatching goods to multiple locations from a single sale order.
    """,
    'category': 'Sales',
    'sequence': 2,
    'author': 'Namah Softech Private Limited',
    'contributors': ['Khanak Hathi'],
    'website': 'http://namahsoftech.com/',
    'license': 'OPL-1',
    'price': 34.99,
    'currency': 'USD',
    'support': 'support@namahsoftech.com',
    'depends': ['sale_management', 'sale_stock', 'stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'report/sale_order_report.xml',
        'report/stock_picking_report.xml',
    ],
    'images': ['static/description/img/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
