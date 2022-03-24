import numpy as np

x = {'id': 'pay_J7eJyI090wpjka',
     'entity': 'payment',
     'amount': 100,
     'currency': 'INR',
     'status': 'captured',
     'order_id': 'order_J7eJYPm9kVEMiW',
     'invoice_id': None,
     'international': False,
     'method': 'upi',
     'amount_refunded': 0,
     'refund_status': None,
     'captured': True,
     'description': None,
     'card_id': None,
     'bank': None,
     'wallet': None,
     'vpa': 'success@razorpay',
     'email': 'vikask99588@gmail.com',
     'contact': '+918920563723',
     'notes': [],
     'fee': 2,
     'tax': 0,
     'error_code': None,
     'error_description': None,
     'error_source': None,
     'error_step': None,
     'error_reason': None,
     'acquirer_data': {'rrn': '586345405507',
                       'upi_transaction_id': 'EC5E83CDD33CE537CD8898DB3B93E46F'},
     'created_at': 1647409424
     }


print(x['acquirer_data']['upi_transaction_id'])
