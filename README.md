# carwash_site
Simple car wash business site with checkout

Elite Car Wash is a basic carwash membership service coded in Python using the Flask framework.

Implemented is a straightforward authentication system which houses the logic for creating a user account and sending an activation email.
The user then has an associated profile which collects basic information, allows password changes and has a link for subscription information.
Subscription information contains the current status of subscription, next payment date (if applicable) and being able to change/cancel the subscription.

Subscriptions are implemented using the [Stripe API](https://stripe.com/docs/api).
