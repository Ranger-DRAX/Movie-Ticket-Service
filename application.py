from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import session, redirect, url_for, render_template, request, flash
import mysql.connector
from flask_mysqldb import MySQL
import base64

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_name'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project_uni'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)


@app.route('/')
def index():
    # Fetch user info from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name, Location FROM user_info WHERE User_ID = 1")  # Adjust User_ID according to your setup
    user_info = cur.fetchone()
    username = user_info[0] if user_info else None
    location = user_info[1] if user_info else None
    return render_template('home.html', username=username, location=location)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM user_info WHERE Name = %s AND Password = %s", (username, password))
        user = cur.fetchone()

        if user:
            # Get user_id from the fetched user
            user_id = user[3]
         
            # print(user_id, len(user))
            # for x in range(len(user)-3):
            #     print(user[x])
                
            
            # Debugging purposes
            # Store user_id in the session
            session['user_id'] = user_id

            # Get column names from cursor description
            columns = [col[0] for col in cur.description]
            user_dict = dict(zip(columns, user))
            username = user_dict['Name']
            location = user_dict['Location']
            return render_template('home.html', username=username, location=location)
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('index'))

    return render_template('login.html')



@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        location = request.form['location']  # Get the selected location

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM user_info WHERE Email = %s", (email,))
        user = cur.fetchone()

        if user:
            flash('Email already exists', 'error')
            return redirect(url_for('register'))

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = base64.b64encode(image_file.read())
            else:
                image_data = None
        else:
            image_data = None

        cur.execute("INSERT INTO user_info (Name, Phone_No, Email, Password, Image, Location) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, phone_no, email, password, image_data, location))  # Include location in the query

        mysql.connection.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('success'))

    return render_template('register.html')

''''

User_profile

'''
@app.route('/user-profile')
def user_profile():
    if 'user_id' not in session:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT Name, Phone_No, Email, Location FROM user_info WHERE User_ID = %s", (session['user_id'],))
    user_info = cur.fetchone()
    cur.close()

    if not user_info:
        flash('User profile not found', 'error')
        return redirect(url_for('index'))

    return render_template('user_profile.html', user_info=user_info)



""""


delete_profile 

"""

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        flash('Please login to delete your profile', 'error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user_info WHERE User_ID = %s", (session['user_id'],))
    mysql.connection.commit()
    cur.close()

    session.pop('user_id', None)  # Remove user_id from session after deletion
    flash('Your profile has been deleted successfully', 'success')
    return redirect(url_for('index'))







@app.route('/movies')
def movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movie")
    movies = cur.fetchall()
    cur.close()

    formatted_movies = []
    for movie in movies:
        # Fetch image data and encode it in base64
        cur = mysql.connection.cursor()
        cur.execute("SELECT poster_data FROM movie WHERE Movie_name = %s", (movie[0],))
        poster_data = cur.fetchone()[0]
        cur.close()

        formatted_movie = {
            'Name': movie[0],
            'Rating': movie[1],
            'Trailer': movie[2],
            'movie_review': movie[3],
            'poster_data': base64.b64encode(poster_data).decode('utf-8')  # Encode image data in base64
        }
        formatted_movies.append(formatted_movie)

    return render_template('movie.html', movies=formatted_movies)




from flask import session, redirect, url_for, render_template, request, flash

@app.route('/booking_ticket', methods=['GET', 'POST'])
def booking_ticket():
    
    if 'user_id' not in session:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))  # Adjust 'login' to your actual login route
    
    if request.method == 'POST':
        
        # Get form data
        date = request.form.get('date')
        show_time = request.form.get('show_time')
        seat_number = request.form.get('seat_number')
        user_id = request.form['user_id']
        #movie_name = request.form.get('movie_name_1')
        #print(date,show_time ,seat_number,user_id, session['movie_name'],session )
        
        # Check if all required fields are present
        if not (date and show_time and seat_number):
            # Missing required fields, handle the error (e.g., display an error message)
            flash("Error: Required form fields are missing.", "error")
            
           #return 0
           # return redirect(url_for('booking_ticket'))
           
        try:
            # Insert data into the ticket table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO ticket (User_ID, Movie_Name, Seat_Number, Movie_Time, Booking_Date) VALUES (%s, %s, %s, %s, %s)",
                        (session['user_id'], session['movie_name'], seat_number, show_time, date))
            mysql.connection.commit()
            cur.close()
            flash("Ticket booked successfully!", "success")
            return redirect(url_for('payment'))
        except Exception as e:
            # Log the error and display an error message
            print("Error inserting ticket data:", str(e))
            flash("Error booking ticket. Please try again later.", "error")
            return redirect(url_for('booking_ticket'))
    if request.method == 'GET':
        return render_template('booking_ticket.html')

@app.route('/booking_ticket_1/<movie_name_1>')
    
def booking_ticket_1(movie_name_1):
    session['movie_name'] = movie_name_1
    return redirect(url_for('booking_ticket'))




@app.route('/success_book_ticket')
def success_book_ticket():
    return render_template('success_book_ticket.html')




     
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))  # Adjust 'login' to your actual login route

    if request.method == 'POST':
        # Get form data
        payment_type = request.form.get('payment_type')
        mobile_no = request.form.get('mobile_no')
        card_no = request.form.get('card_no')
        payment_date = request.form.get('payment_date')
        user_id = session['user_id']  # Get user_id from the session

        print(payment_type, mobile_no, card_no, payment_date, user_id)#for debugging purposes

        # Checking for required fields
        if payment_type == 'Credit Card' and not card_no:
            flash("Error: Credit Card Number is required.", "error")
            return redirect(url_for('payment'))
        elif payment_type == 'Mobile Banking' and not mobile_no:
            flash("Error: Mobile Number is required.", "error")
            return redirect(url_for('payment'))

        try:
            # Insert data into the payment table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO payment (payment_type, mobile_no, card_no, payment_date, user_id) VALUES (%s, %s, %s, %s, %s)",
                        (payment_type, mobile_no, card_no, payment_date, user_id))
            mysql.connection.commit()
            cur.close()
            flash("Payment successful!", "success")
            return redirect(url_for('payment_success'))
        except Exception as e:
            # Log the error and display an error message
            print("Error inserting payment data:", str(e))
            flash("Error booking payment. Please try again later.", "error")
            return redirect(url_for('payment'))

    if request.method == 'GET':
        return render_template('payment.html', user_id=session['user_id'])
        

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('index')) 




@app.route('/payment_method', methods=['POST'])
def process_payment():
    # Process payment data
    # Insert payment data into the database
    # Assuming payment_id and user_id are obtained from the form data or session
    payment_id = request.form['payment_id']
    user_id = request.form['user_id']

    # Redirect to payment success page
    return redirect(url_for('payment_success', payment_id=payment_id, user_id=user_id))

@app.route('/payment_success')
def payment_success():
    # Render the payment success template
    return render_template('payment_success.html')


@app.route('/fanclub')
def fanclub():
    return render_template('fanclub.html')



@app.route('/about_us')
def about_us():
    return render_template('about_us.html')




if __name__ == '__main__':
    app.run(debug=True)
