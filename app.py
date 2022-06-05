from flask import Flask, url_for, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    body = f'''
        <h1>Select a receipt:</h1><br>

        <a href="{ url_for('receipt', receipt='how to make a coffee.txt', number=0) }">how to make a cofee</a><br>
        <a href="{ url_for('receipt', receipt='how to make a tea.txt', number=0) }">how to make a tea</a><br><br>

        <a href="{ url_for('leave_comment') }">Leave a comment</a><br>
        <a href="{ url_for('show_comments') }">Show all comments</a><br>
    '''

    return body

@app.route('/leave_comment', methods=['GET', 'POST'])
def leave_comment() :
    if request.method == 'GET':
        body = f'''
            <form id="leave_comment" action="{ url_for('leave_comment') }" method="POST"
                <label for="leave_comment">Leave Comment</label><br>
                <textarea id="comment" name="comment" rows="3" cols="50">
                </textarea><br><br>
                <input type="submit" value="Send and return home">
            </form>
        '''
        return body
    else:
        comment = '...'
        if 'comment' in request.form:
            comment = request.form['comment']

        comments_file = os.path.join(app.static_folder, 'comments/comments.txt')
        with open(comments_file, 'a') as file:
            if "<" in comment:
                comment = comment.replace('<', '&lt')
            if ">" in comment:
                comment = comment.replace('>', '&gt')   

            file.write(comment)
            file.write('\n')

        return redirect(url_for('index'))

@app.route('/show_comments')
def show_comments():
    comment = '<ul>'
    comments_file = os.path.join(app.static_folder, 'comments/comments.txt')
    print(comments_file)
    with open(comments_file, 'r') as file:
        for line in file.readlines():
            if line != '\n':
                comment = comment + '\n<li>' + line + '</li>'
        comment = comment + '\n</ul>'    
    
    body = f'''
        <h1>The comments:</h1>
        {comment}<br>
        <a href="{ url_for('index') }">Back to home</a>
    '''

    return body

@app.route('/<string:receipt>/<int:number>')
def receipt(receipt, number):
    path = os.path.join(app.static_folder, receipt)
    
    with open(path, 'r') as file:
        lines_len = len(file.readlines()) - 1

    with open(path, 'r') as file:
        line = file.readlines()[number]
        body = f'''
            <h1>The step {number + 1} for receipt {receipt.rstrip('.txt')}:</h1>
            {line}<br>

            <ul>
                <li><a href="{ url_for('index') }">Home</a></li>
        '''
        print(lines_len)
        if number < lines_len:
            body = body + f'''<li><a href="{ url_for('receipt', receipt=receipt, number=number+1) }">Next</a></li>'''
        if number > 0:
            body = body + f'''<li><a href="{ url_for('receipt', receipt=receipt, number=number-1) }">Previous</a></li>'''
        body = body + "</ul>"
        
    return body

if __name__ == '__main__':
    app.run(debug=True)