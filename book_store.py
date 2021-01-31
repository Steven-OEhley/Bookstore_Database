### Bookstore Database Project ###

# ========================================
# Step 1: Importing the Necessary Packages
# ========================================

# import sqlite3 - create database
# import os - help check files
import sqlite3
import os

# ============================
#Step 2: Inital database setup
# ============================

# database setup skipped if database file already exists
# skipped using if condition
# if bookstore_db exists skips below code block else executes
# used os to check if db is file

if os.path.isfile("bookstore_db"):
	db = sqlite3.connect('bookstore_db')
	cursor = db.cursor()
	print("\nDatabase Opened and ready to query....")
else:
	# create cursor object 
	# create book table

	# create database for bookstore
	# connect if already created
	# create cursor object
	db = sqlite3.connect('bookstore_db')
	cursor = db.cursor()

	# create cursor object 
	# create book table
	cursor.execute('''
		CREATE TABLE books (book_id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
		''')

	db.commit()

	# enter database info
	initial_data = [(3001,"A Tale of Two Cities","Charles Dickens",30),
	(3002,"Harry Potter and the Philospher's Stone","J.K Rowling",40),
	(3003,"The Lion, The Witch and The Wardrobe","C.S Lewis",25),
	(3004,"The Lord of The Rings","J.R.R Tolkien",37),
	(3005,"Alice in Wonderland","Lewis Carroll",12)]

	cursor.executemany(''' INSERT INTO books (book_id,Title, Author, Qty) VALUES(?,?,?,?)''',
		initial_data)

	db.commit()
	print("\nDatabase has been created and initial data has been entered")
	print("Database opened and ready for query....")

# ===========================================
# Step 3: Building out Functions for the user
# ===========================================

# 1 - function to enter a book
def enter_book():
	'''Takes in information about a book and enters it into the data base
	parameters - None
	Returns - None. 
	Prints what has been added to the db.'''
	
	# automatically assign a book_id based on value of last row in table
    # select max(id) returns the largest id in the databse
    # fetchone returns the first row from the select statement (a tuple)
    # fetchone[0] first element of fetchone
	cursor.execute('SELECT max(book_id) FROM books')
	book_id = int(cursor.fetchone()[0])+1
    # get user input for the remaining attributes
	book_title = input("\nPlease enter the Title of the book ")
	book_author = input("\nPlease enter the Author of the book ")
	book_stock = int(input("\nPlease enter the stock on hand "))

	print("\nPlease confirm you are happy with the entered information ")
	print(f'''    
        book_title: {book_title}
        book_author: {book_author}
        Stock on hand: {book_stock}''')
	print('''\nIf you are happy please enter Y
If you would like to make a change to the given information please enter one of the below:
- Enter title to change the title
- Enter author to change the author 
- Enter stock to change the stock on hand''')

	user_continue = input("\nPlease enter your choice now ")

	# by using the if else condition it allows the user the opportunity to edit the given information before proceeding
	# used .strip() .lower() on user input to elimate capitalisation and white space issues
	if user_continue.strip().lower() == "y":
		print("\nContinuing with original input....") 
	elif user_continue.strip().lower() == "title":
		book_title = input("\nPlease enter the new Title of the book ")
	elif user_continue.strip().lower() == "author":
		book_author = input("\nPlease enter the new Author of the book ")
	elif user_continue.strip().lower() == "stock":
		book_stock = int(input("\nPlease enter the ammended stock on hand "))
	else:
		print('''\nYou did not enter a valid input.
Continuing with your original selection. 
You can always update your entry with the UPDATE FUNCTION later if there is something you would like to change''')

	book_info = [(book_id,book_title,book_author,book_stock)]

	# enter book ifno into database

	cursor.executemany(''' INSERT INTO books (book_id,Title, Author, Qty) VALUES(?,?,?,?)''',
		book_info)
	db.commit()

	# inform the user of the changes
	print("\nThe book has been successfully added to the data base")
	print(f"The book was assigned a book_id of {book_id} in the database")
	print("\nData base is updated and ready for query....")


# 2 - function to update a book
def update_book():
	'''Takes in new information about a book and replaces the the information in the database
	Allows user to search via title or author 
	Then displays all matches and requests the unique book_id in the event that the search returns more 
	than one result for an author or title. This ensures correct book is updated
	Search by title and author rather than book_id as it is very unlikely a store clerk could remember every unique book_id 
	when the database becomes larger
	parameters - None
	Returns - None. 
	Prints what has been amended in the db, displaying previous info and new updated info.'''

	print(" \nYou want to update a book, do you want to search by the author or the book title?")
	search_item = input(" To search by author - Enter a\n To search by title - Enter t ")

	if search_item.strip().lower() == "a":

		# ask user if they know the full author name or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the authors initials and surname or do you only know part of the name?")
		partial_or_full = input("If you know the full details of the author enter full, otherwise press enter and a search on a partial name will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results

			while True:

				author_search = input("Please enter the authors full name")
				print ("\nThe database contains the below results for the author")

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE author=?''', (author_search,))

				if cursor is None:
					print("The database has no results for that author")
					print("Double check your spelling and try again")
					continue

				else:

					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full author name
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				author_search = input("\nPlease enter the known piece of the author's name to search ")
				wild_card_search = "%"+author_search+"%"

				cursor.execute('''SELECT * FROM books WHERE author LIKE ?''', (wild_card_search,))
				
				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be printed below:")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())
			
			
		# based on book_id retrieve the previous database info
		cursor.execute('''SELECT * FROM books WHERE book_id=?''', (book_to_change,))

		old_info = cursor.fetchone()
		old_title = old_info[1]
		old_author = old_info[2]
		old_stock = old_info[3]

		# request updated information from the user
		print("\nPlease enter the new information for the book")
		print("If you want to leave a value unchanged please enter the previous value")

		book_title = input("\nPlease enter the previous or ammended Title of the book ")
		book_author = input("\nPlease enter the previous or ammended Author of the book ")
		book_stock = int(input("\nPlease enter the previous or ammended Stock on hand "))

		# add changes to the database

		cursor.execute(''' UPDATE books SET Title = ?,Author = ?,Qty = ? WHERE book_id = ? ''', (book_title,book_author,book_stock,book_to_change))
		db.commit()

		print(f"\nThank you, the below changes have been made to book_id: {book_to_change}")
		print("The information has been changed FROM:")
		print(f'''Title: {old_title}
Author: {old_author}
Stock on Hand: {old_stock}''')
		print("\nThe information has been changed TO:")
		print(f'''Title: {book_title}
Author: {book_author}
Stock: {book_stock}''')
		print("\nDatabase updated and ready for query....")


	elif search_item.strip().lower() == "t":

		# ask user if they know the full title or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the full title or only the beginning?")
		partial_or_full = input("If you know the full title enter full otherwise press enter and a search on a partial title will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results
			
			while True:

				title_search = input("Please enter the full title")
				

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE title=?''', (title_search,))

				if cursor is None:
					print("The database has no results for that title")
					print("Double check your spelling and try again")
					continue

				else:

					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full title
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				title_search = input("\nPlease enter the portion of the title that is known ")
				wild_card_search = "%"+title_search+"%"
				
				cursor.execute('''SELECT * FROM books WHERE title LIKE ?''', (wild_card_search,))
				

				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be printed below:")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the books unique book_id ").strip())
			
			
		# based on book_id retrieve the previous database info
		cursor.execute('''SELECT * FROM books WHERE book_id=?''', (book_to_change,))
		old_info = cursor.fetchone()
		old_title = old_info[1]
		old_author = old_info[2]
		old_stock = old_info[3]


		# request updated information from the user
		print("\nPlease enter the new information for the book")
		print("If you want to leave a value unchanged please enter the previous value")

		book_title = input("\nPlease enter the previous or ammended Title of the book ")
		book_author = input("\nPlease enter the previous or ammended Author of the book ")
		book_stock = int(input("\nPlease enter the previous or ammended Stock on hand "))

		# add changes to the database

		cursor.execute(''' UPDATE books SET Title = ?,Author = ?,Qty = ? WHERE book_id = ? ''', (book_title,book_author,book_stock,book_to_change))
		db.commit()

		print(f"\nThank you, the below changes have been made to book_id: {book_to_change}")
		print("The information has been changed FROM:")
		print(f'''Title: {old_title}
Author: {old_author}
Stock on Hand: {old_stock}''')
		print("\nThe information has been changed TO:")
		print(f'''Title: {book_title}
Author: {book_author}
Stock: {book_stock}''')


		print("\nData base updated and ready for query....")

	else:
		print("\nYou did not enter a valid input")
		print("No changes made")
		print("\nData base ready for query....")


# 3 - function to delete a book
def delete_book():
	'''Deletes a given book from the database and resets the book_id index after removing the book
	Allows user to search via title or author 
	Then displays all matches and requests the unique book_id in the event that the search returns more 
	than one result for an author or title. This ensures correct book is updated
	Search by title and author rather than book_id as it is very unlikely a store clerk could remember every unique book_id 
	when the database becomes larger
	parameters - None
	Returns - None. 
	Prints that entry has been deleted and that the index has been reset.'''

	print("\nYou want to delete a book, do you want to search by the author or the book title?")
	search_item = input(" To search by author - Enter a\n To search by title - Enter t ")

	if search_item.strip().lower() == "a":

		# ask user if they know the full author name or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the authors initials and surname or do you only know part of the name?")
		partial_or_full = input(" If you know the full details of the author enter full, otherwise press enter and a search on a partial name will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results

			while True:

				author_search = input("Please enter the authors full name ")
				print ("\nThe database contains the below results for the author")

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE author=?''', (author_search,))

				if cursor is None:
					print("The database has no results for that author")
					print("Double check your spelling and try again")
					continue

				else:

					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full author name
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				author_search = input("\nPlease enter the known piece of the author's name to search ")
				wild_card_search = "%"+author_search+"%"

				cursor.execute('''SELECT * FROM books WHERE author LIKE ?''', (wild_card_search,))
				
				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be printed below:")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())
			
		
		# delete selected book
		# commit to database	
		cursor.execute('''DELETE FROM books WHERE book_id = ?''', (book_to_change,))
		db.commit()

		# book_id would now no longer be sequential
		# example deleted book_id 3002 
		# book_id would read 3001, 3003, 3004 etc
		## Want to add functionality that would reset the index and renumber from 3001
		 # will look at adding this in the future as I have not been able to find a solution 
		print("Selected book has been removed from the database")
		print("Database has been updated and is ready for query")

	elif search_item.strip().lower() == "t":

		# ask user if they know the full title or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the full title or only the beginning?")
		partial_or_full = input("If you know the full title enter full otherwise press enter and a search on a partial title will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results
			
			while True:

				title_search = input("Please enter the full title")
				

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE title=?''', (title_search,))

				if cursor is None:
					print("The database has no results for that title")
					print("Double check your spelling and try again")
					continue

				else:

					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full title
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				title_search = input("\nPlease enter the portion of the title that is known ")
				wild_card_search = "%"+title_search+"%"
				
				cursor.execute('''SELECT * FROM books WHERE title LIKE ?''', (wild_card_search,))
				

				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be printed below:")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the books unique book_id ").strip())
			
			
		cursor.execute('''DELETE FROM books WHERE book_id = ?''', (book_to_change,))
		db.commit()

		print("\nSelected book has been removed from the database")
		print("Database has been updated and is ready for query")


	else:
		print("\nYou did not enter a valid input")
		print("No changes made")
		print("\nData base ready for query....")



# 4 - Function to search books
def search_book():

	'''Allows user to search via title or author. Then displays all matches.
	parameters - None
	Returns - None. 
	Prints that entry has been deleted and that the index has been reset.'''

	print("Let's Search the Database")
	search_item = input(" To search by author - Enter a\n To search by title - Enter t")

	if search_item.strip().lower() == "a":

		# ask user if they know the full author name or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the authors initials and surname or do you only know part of the name?")
		partial_or_full = input(" If you know the full details of the author enter full, otherwise press enter and a search on a partial name will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results

			while True:

				author_search = input("Please enter the authors full name")
				print ("\nThe database contains the below results for the author")

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE author=?''', (author_search,))

				if cursor is None:
					print("The database has no results for that author")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be displayed below:\n ")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full author name
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				author_search = input("\nPlease enter the known piece of the author's name to search ")
				wild_card_search = "%"+author_search+"%"

				cursor.execute('''SELECT * FROM books WHERE author LIKE ?''', (wild_card_search,))
				
				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be displayed below:\n")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break
	
	elif search_item.strip().lower() == "t":

		# ask user if they know the full title or only a portion
		# if only a portion implement wildcards in the search and direct user to then search off of book_id

		print("\nDo you know the full title or only the beginning?")
		partial_or_full = input("If you know the full title enter full otherwise press enter and a search on a partial title will be done")
		
		if partial_or_full.strip().lower() == "full":

			# added check to ensure database contains search results
			
			while True:

				title_search = input("Please enter the full title")
				

				# display all matches for the author
				cursor.execute('''SELECT * from books WHERE title=?''', (title_search,))

				if cursor is None:
					print("The database has no results for that title")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be displayed below:\n ")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

			print("\nPlease select your book from the above")
			book_to_change = int(input("Enter the book's unique book_id ").strip())

		else:

			# make use of wildcards in search
			# in the event that the store clerk did not have the full title
			# added check for if the user results returns nothing in the event of a partial entry

			while True:

				title_search = input("\nPlease enter the portion of the title that is known ")
				wild_card_search = "%"+title_search+"%"
				
				cursor.execute('''SELECT * FROM books WHERE title LIKE ?''', (wild_card_search,))
				

				if cursor is None:
					print("\nThe Database contains no similar search results")
					print("Double check your spelling and try again")
					continue

				else:
					print("Search results will be displayed below:\n ")
					for row in cursor:
						print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
					break

	else:
		print("\nYou did not enter a valid input")
		print("No changes made")
		print("\nData base ready for query....")

# 5 - Stock Query Function

def stock_query():

	'''
	The function takes a stock value
	The functions then allows one to return all stock either:
	- >= given stock value
	- <= given stock value
	- = given stock value
	'''

	stock_search = input("\nWhat is the stock value you want to query? ")
	print("Do you want to return results greater than,less than or equal to your given units?")
	over_under = input("Enter over to return results greater than and equal to your value\nEnter under to return results less than and equal to your value\nEnter equal to return only results that match your input units ")

	if over_under.strip().lower() == "under":
		cursor.execute('''SELECT * FROM books WHERE qty <= ?''',(stock_search,))
		print("\nThe below items were returned:")
		for row in cursor:
			print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")

	elif over_under.strip().lower() == "over":
		cursor.execute('''SELECT * FROM books WHERE qty >= ?''',(stock_search,))
		print("\nThe below items were returned:")
		for row in cursor:
			print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")

	elif over_under.strip().lower() == "equal":
		cursor.execute('''SELECT * FROM books WHERE qty = ?''',(stock_search,))
		print("\nThe below items were returned:")
		for row in cursor:
			print(f"book_id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Stock: {row[3]}")
	else:
		print("\nYou did not enter a valid input")
		print("No changes made")
		print("\nData base ready for query....")


# ==============================
# Step 4: Setting up the program
# ==============================

while True:
	print("\nDatabase running....")
	print('''
		\nWhich of the following would you like to do?
		- 1. Enter Book
		- 2. Update Book
		- 3. Delete Book
		- 4. Query Stock on Hand
		- 5. Close and Exit''')
	user_action = int(input("Enter the corresponding number "))

	if user_action == 1:
		enter_book()
		continue
	elif user_action == 2:
		update_book()
		continue
	elif user_action == 3:
		delete_book()
		continue
	elif user_action == 4:
		stock_query()
		continue
	elif user_action == 5:
		db.close()
		print("\nDatabase has been closed")
		break
	else:
		print("\nYou did not enter a valid response\nPlease try again")
		continue















