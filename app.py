from flask import Flask, render_template, request, flash, redirect, url_for, session

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
        'description': 'Ang among standard nga serbisyo. Hugas, uga, ug pilo nga limpyo. (Our standard service: Wash, dry, and clean fold.)',
        'details': 'Presyo kada kilo. 24-oras mahuman. (Priced per kilogram. 24-hour turnaround.)',
        'price_per_unit': '₱45 / kg',
        'detergent_cost': '₱5 (Included in the ₱45 price)'
    },
    'dry_cleaning': {
        'name': 'Premium Dry Cleaning',
        'icon': '👔',
        'description': 'Para sa formal wear ug delicado nga sanina. Segurado nga walay gisi. (For formal wear and delicate clothes. Guaranteed not to tear.)',
        'details': 'Presyo kada butang. Apil na ang pressing. (Priced per item. Pressing is included.)',
        'price_per_unit': '₱150 / item',
        'detergent_cost': '₱20 (Specialized solvent)'
    },
    'bedding_bulky': {
        'name': 'Bedding & Bulky Items',
        'icon': '🛌',
        'description': 'Para sa kumot, habol, ug dagko nga sanina. (For comforters, blankets, and big clothes.)',
        'details': 'Fixed nga presyo kada butang. Gamit ang dagkong makina. (Fixed pricing per item. Uses large machines.)',
        'price_per_unit': '₱300 / item',
        'detergent_cost': '₱35 (Heavy duty detergent)'
    }
}


# --- ROUTES ---

# Home/Index Route
@app.route('/')
def index():
    return render_template('index.html', logged_in='user' in session)


# --- AUTHENTICATION ROUTES (Login/Sign In) ---

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')

        if action == 'login':
            if email in DUMMY_USERS and DUMMY_USERS[email] == password:
                session['user'] = email  # Store user in session
                flash('Salamat sa pag Log In! Welcome back. (Thank you for logging in!)', 'success')
                return redirect(url_for('index'))  # <<-- Redirects to Home after successful login
            else:
                flash(
                    'Log In failed. Palihug check sa imong email ug password. (Please check your email and password.)',
                    'error')

        elif action == 'signup':
            if email in DUMMY_USERS:
                flash(
                    'Kining email naka register na. Palihug Log In. (This email is already registered. Please log in.)',
                    'error')
            else:
                DUMMY_USERS[email] = password
                session['user'] = email
                flash('Sign Up successful! Karon naka log in na ka. (You are now logged in.)', 'success')
                return redirect(url_for('index'))

    return render_template('auth.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Naka log out na ka. (You have been logged out.)', 'info')
    return redirect(url_for('index'))


# --- NEW ABOUT US ROUTE ---
@app.route('/about_us')
def about_us():
    return render_template('about_us.html', logged_in='user' in session)


# --- OTHER ROUTES ---
@app.route('/services')
def services():
    return render_template('services.html', services=SERVICE_DATA.values(), logged_in='user' in session)


@app.route('/inquire', methods=['GET', 'POST'])
def inquire():
    if request.method == 'POST':
        # In a real app, you would send this inquiry to your email/database
        print(f"NEW INQUIRY: {request.form}")
        flash(
            'Ang imong inquiry na send na! Among kontakon ka dayon. (Your inquiry has been sent! We will contact you right away.)',
            'success')
        return redirect(url_for('index'))

    return render_template('inquire.html', services=SERVICE_DATA.values(), logged_in='user' in session)


@app.route('/delivery')
def delivery():
    if 'user' not in session:
        flash('Palihug Log In aron ma track ang imong delivery. (Please log in to track your delivery.)', 'error')
        return redirect(url_for('auth'))

    status = "Ang imong laundry kay ginahugasan pa. Delivery: Ugma, 4 PM. (Your laundry is currently being washed. Delivery: Tomorrow, 4 PM.)"
    return render_template('delivery.html', status=status, logged_in=True)


# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)