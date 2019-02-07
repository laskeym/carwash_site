#######################################
# Helper functions for the stripe API #
#######################################

import stripe

def createCustomer(email, token):
    """
    Creates a Stripe API Customer resource
    """
    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    return customer.id

def createSubscription(customer_id, plan):
    """
    Creates a Stripe API Subscription resource
    """
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[
          {
            "plan": plan
          }
        ]
    )

    return subscription.id