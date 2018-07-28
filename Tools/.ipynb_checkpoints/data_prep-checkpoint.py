def overview_selected_files(path, file_ending):
	'''
	Overview ..
	'''
	for file in os.listdir(path):
		if file.endswith(file_ending):
			print(os.path.join('found files :', file)) 
				
            
def paths_selected_files(path, file_ending):
    '''
    Get paths for selected files
    '''
    path_books_list = [os.path.join(path, file) 
                       for file in os.listdir(path) if file.endswith(file_ending)]
    print(path_books_list)
    return path_books_list


def open_book_list(path_books_list):
    '''
    Open book list
    '''
    book_list = [open(file).read() for file in path_books_list]
    
    [print('Book #{book_n} has a word length of {book_text}'.format(
    book_n=book_n, book_text=len(book_text))) 
                     for book_n, book_text in enumerate(book_list)]
    return book_list
