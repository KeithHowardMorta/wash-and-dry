from flask import Flask, render_template, request, flash, redirect, url_for, session, abort

app = Flask(__name__)
# Crucial for sessions (login status) and flash messages
app.secret_key = 'wash_and_dry_super_secret_key'

# --- DUMMY DATA ---
# Dummy user data for login simulation
DUMMY_USERS = {'keith@example.com': 'password123', 'test@user.com': '1234'}

# Detailed service information with detergent pricing
SERVICE_DATA = {
    'wash_and_fold': {
        'name': 'Standard Wash & Fold',
        'icon': '👕',
        'description': ' (Our standard service: Wash, dry, and clean fold.)',
        'details': ' (Priced per kilogram. 24-hour turnaround.)',
        'price_per_unit': '₱45 / kg',
        'detergent_cost': '₱5 (Included in the ₱45 price)'
    },
    'dry_cleaning': {
        'name': 'Premium Dry Cleaning',
        'icon': '👔',
        'description': ' (For formal wear and delicate clothes. Guaranteed not to tear.)',
        'details': ' (Priced per item. Pressing is included.)',
        'price_per_unit': '₱150 / item',
        'detergent_cost': '₱20 (Specialized solvent)'
    },
    'bedding_bulky': {
        'name': 'Bedding & Bulky Items',
        'icon': '🛌',
        'description': '. (For comforters, blankets, and big clothes.)',
        'details': ' (Fixed pricing per item. Uses large machines.)',
        'price_per_unit': '₱300 / item',
        'detergent_cost': '₱35 (Heavy duty detergent)'
    }
}


# ----------------------------------------------------
# *** KEY CHANGE: AUTHENTICATION GUARD FUNCTION ***
# Kini nga function maoy mo-check kung naka-login ba ang user.
# Kini ang atong gamiton sa mga routes nga gusto natong i-protect.
# ----------------------------------------------------
def login_required():
    if 'user' not in session:
        # Flash message para makabalo ang user nga kinahanglan siya mo-login.
        flash(' (Need to fill up to go can I get a kiss goodnight baby?.)', 'error')
        # E-redirect ang user sa auth page.
        return redirect(url_for('auth'))
    # Kung naka-login, mo-return og None ug mo-padayon ang function sa route.
    return None


# --- ROUTES ---

# Home/Index Route - Karon PROTECTED na
@app.route('/')
def index():
    auth_check = login_required()
    if auth_check:
        return auth_check  # Mo-redirect sa auth page

    # Kung naka-login, mo-render sa index.html
    return render_template('index.html', logged_in='user' in session)


# --- AUTHENTICATION ROUTES (Login/Sign Up) ---

# 1. AUTH DISPLAY PAGE (GET request only) - Kining page ra ang DILI PROTECTED
@app.route('/auth', methods=['GET'])
def auth():
    if 'user' in session:
        # Kung naka-login na, E-REDIRECT sa Home Page dayon.
        return redirect(url_for('index'))

    # Kung wala pa naka-login, ipakita ang login/signup form.
    return render_template('auth.html')


# 2. LOGIN HANDLING (POST request)
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email in DUMMY_USERS and DUMMY_USERS[email] == password:
        session['user'] = email  # Store user in session
        flash(' (Thank you for logging in! Welcome to Wash & Dry.)', 'success')
        # LOGIN SUCCESS: E-REDIRECT sa Home Page
        return redirect(url_for('index'))
    else:
        flash(
            '(Wrong Email or Password. Please check it carefully.)',
            'error')
        # LOGIN FAILURE: E-REDIRECT balik sa Auth Page
        return redirect(url_for('auth'))


# 3. SIGNUP HANDLING (POST request)
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    if email in DUMMY_USERS:
        flash(
            '(Email that your using,is registered. Please log in.)',
            'error')
        # SIGNUP FAILURE: E-REDIRECT balik sa Auth Page
        return redirect(url_for('auth'))
    else:
        # Sign up success: add user
        DUMMY_USERS[email] = password
        flash(' (thank you! Registered successfully. Now, Please Log In.)', 'success')
        # SIGNUP SUCCESS: E-REDIRECT sa Auth Page (para maka-Log In)
        return redirect(url_for('auth'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash(' (you have been logged out. Thank you for using our website.)', 'info')
    return redirect(url_for('auth'))  # E-redirect sa auth page pagkahuman og logout.


# --- NEW ABOUT US ROUTE - Karon PROTECTED na ---
@app.route('/about_us')
def about_us():
    auth_check = login_required()
    if auth_check:
        return auth_check
    return render_template('about_us.html', logged_in='user' in session)


# --- OTHER ROUTES - Karon PROTECTED na ---
@app.route('/services')
def services():
    auth_check = login_required()
    if auth_check:
        return auth_check
    return render_template('services.html', services=SERVICE_DATA.values(), logged_in='user' in session)


@app.route('/inquire', methods=['GET', 'POST'])
def inquire():
    auth_check = login_required()
    if auth_check:
        return auth_check

    if request.method == 'POST':
        # Makuha nato ang tanang data gikan sa form, apil ang bag-ong fields.
        inquiry_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'contact': request.form.get('contact'),
            'weight': request.form.get('weight'),
            'payment': request.form.get('payment_method'),
            'service': request.form.get('service'),
            'message': request.form.get('message'),
        }

        # In a real app, you would send this inquiry to your email/database
        print(f"--- NEW LAUNDRY INQUIRY RECEIVED ---")
        for key, value in inquiry_data.items():
            print(f"{key.capitalize()}: {value}")
        print(f"------------------------------------")

        flash(
            ' (your inquiry is under proccess! We will contact you as soon as possible.)',
            'success')
        return redirect(url_for('index'))

    return render_template('inquire.html', services=SERVICE_DATA.values(), logged_in='user' in session)


@app.route('/delivery')
def delivery():
    auth_check = login_required()
    if auth_check:
        return auth_check

    status = " (your cloaths is under proccess. Delivery: tomorrow, At 4pm in the afternoon)"
    return render_template('delivery.html', status=status, logged_in=True)


# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)