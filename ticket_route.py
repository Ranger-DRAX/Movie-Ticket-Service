



''''

process--2



'''




@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    
    if request.method == 'POST':
        # Handle ticket booking form submission here
        user_id =  request.form.get('user_id')
        movie_name = request.form.get('movie_name')
        #payment_id = get_payment_id(user_id)
        seat_number = request.form.get('seat_number')
        movie_time = request.form.get('movie_time')
        booking_date = request.form.get('booking_date')

        
        print (user_id , movie_name , seat_number , movie_name, booking_date )
        cur = mysql.connection.cursor()
        
        
        cur.execute("SELECT * FROM user_info WHERE User_ID = %s", (user_id,))
        result = cur.fetchone()
        if result == None: 
            flash('User ID does not exist!', 'error')

            return redirect(url_for('index'))

        cur.execute("INSERT INTO ticket (User_ID, Movie_Name,  Seat_Number, Movie_Time, Booking_Date) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, movie_name,  seat_number, movie_time, booking_date))
        mysql.connection.commit()
        cur.close()

        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('payment_method'))

    seats = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'],
        'B': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10'],
        'C': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
        'D': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
        'E': ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10']
    }

    return render_template('ticket.html', seats=seats)




def get_payment_id(user_id):
    # Generate a unique payment_id using UUID
    payment_id = str(uuid.uuid4())[:10]  # Adjust the length of the payment_id as needed
    return payment_id




''''

process--1



'''



@app.route('/booking_ticket', methods=['GET', 'POST'])
def booking_ticket():
    if request.method == 'POST':
        # Get form data
        date = request.form['booking_date']
        show_time = request.form['showtime']
        seat_number = request.form['seat_number']
        user_id = request.form['user_id']
        movie_name = request.form['movie_name']
        print (user_id , movie_name , seat_number ,date , show_time )
        # Insert data into the ticket table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ticket (user_id, movie_name, seat_Number, Movie_Time, Booking_Date) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, movie_name, seat_number, show_time, date))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('success_book_ticket'))

    return render_template('booking_ticket.html', user_id=session.get('user_id'), movie_name=session.get('movie_name'))