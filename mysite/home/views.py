from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import messageModel
from django.core.validators import validate_email
from django.contrib import messages
from .tictactoe import TicTacToe
import random

# Create your views here.
def home(request):
    about_me = "I am a student studying computer science at NYU Tandon School of Engineering. I am passionate about" \
               " anything I do and love the interactive process of learning through projects. My plan for the future" \
               ", through all my work is to learn as much I can from each experience and improve my capability to" \
               " create and help others."

    experience = "I have multiple years of" \
               " programming experience and have worked heavily with languages such as python, HTML/CSS, and Javascript." \
               " I also have good experience with webapp frameworks (Django) and other useful libraries (OpenCV)." \


    return render(request, 'home/content.html', {'about_me': about_me, 'experience': experience})

def test(request):
    return render(request, 'home/test.html')


def apriltag(request):
    description = "The task for this project was to allow a remote control station to determine the location of a " \
                  "lunar rover. Apriltags were used to provide spacial data about the rover due to their non-reliance " \
                  "on communication between the rover and control station. 6 unique apriltags were aligned with " \
                  "the sides of the rover and were positioned symmetrically to one another." \
                  " A webcam was calibrated and used the homography values of the apriltags to determine their " \
                  "position and orientation."
    return render(request, 'home/apriltag.html', {'description': description})


def cliqueio(request):
    description = "Clique.io is a website designed for college students who are looking for a quick and intuitive " \
                  "platform to promote their ideas and easily gather people for their cause. The website features " \
                  "an effective system to search and sort through many startup ideas to allow students to find what " \
                  "interests them. Students can also create their own posts and set unique keywords to influence " \
                  "their posts in the search algorithm. Post creators can further customize their content by creating " \
                  "their own application questions to fine tune their acceptance process."

    description2 = "When a post is applied to, a notification is sent to the owner of the post, and the applied user " \
                   "can be seen in the owner's post window. Here, the owner can view applicant profiles and manage their " \
                   "applications. The owner can then accept applicants and begin a chat with them using our live chat " \
                   "feature and connect using outside platforms. Clique.io is designed as a versatile and community " \
                   "based solution for college students who want better opportunities to promote their idea."


    return render(request, 'home/cliqueio.html', {'description': description, 'description2': description2})


def contact(request, data=None):
    if data is not None:
        name = data['name']
        subject = data['subject']
        description = data['description']
        return render(request, 'home/contact.html', {'name': name, 'subject': subject, 'description': description})
    else:
        return render(request, 'home/contact.html', {})


def tictactoe_info(request):
    description = "A tic tac toe game where you play against the computer!"

    return render(request, 'home/tictactoeinfo.html', {'description': description})


def tictactoe_game(request, row=-1, col=-1, state=None, user=-1):
    message = ''
    conversion = {1: "-",
                  2: "X",
                  3: "O"}

    if state is None:
        state = 111111111
        modified_board = zip([
                        zip(["-", "-", "-"], [0, 1, 2]),
                        zip(["-", "-", "-"], [0, 1, 2]),
                        zip(["-", "-", "-"], [0, 1, 2])],
                            [0, 1, 2])

        user = 2

    else:
        state = str(state)
        location = 3 * row + col
        state = state[:location] + str(user) + state[location + 1:]
        board = [
            [conversion[int(state[0])], conversion[int(state[1])], conversion[int(state[2])]],
            [conversion[int(state[3])], conversion[int(state[4])], conversion[int(state[5])]],
            [conversion[int(state[6])], conversion[int(state[7])], conversion[int(state[8])]]
        ]
        board[row][col] = conversion[user]

        if user == 2:
            bot = 3
        elif user == 3:
            bot = 2

        first_turn = True
        count = 0

        for row_elem in board:
            for col_elem in row_elem:
                if col_elem == "-":
                    count += 1
                if col_elem == conversion[bot]:
                    first_turn = False

        if count > 0:
            game = TicTacToe(board, first_turn)
            res = game.algorithm(conversion[bot], board)[0]

            winlose = game.check_complete(board)
            print("a", winlose, board)

            if winlose == 2:
                message = "You Win!"
                modified_board = zip([
                    zip(board[0], [0, 1, 2]),
                    zip(board[1], [0, 1, 2]),
                    zip(board[2], [0, 1, 2])], [0, 1, 2])
                return render(request, 'home/tictactoegame.html',
                              {'board': modified_board, 'state': state, 'user': user,
                               'message': message})

            location = 3 * res[0] + res[1]
            board[res[0]][res[1]] = conversion[bot]
            winlose = game.check_complete(board)
            print("b", winlose, board)

            if winlose == 1:
                message = "You lose :("
                modified_board = zip([
                    zip(board[0], [0, 1, 2]),
                    zip(board[1], [0, 1, 2]),
                    zip(board[2], [0, 1, 2])], [0, 1, 2])
                return render(request, 'home/tictactoegame.html',
                              {'board': modified_board, 'state': state, 'user': user,
                               'message': message})

            print(winlose, "lose or win")

            state = state[:location] + str(bot) + state[location + 1:]
            print(state, row, col, res)
        else:
            message = "Tie!"

        modified_board = zip([
            zip(board[0], [0, 1, 2]),
            zip(board[1], [0, 1, 2]),
            zip(board[2], [0, 1, 2])], [0, 1, 2])

        state = int(state)

    return render(request, 'home/tictactoegame.html', {'board': modified_board, 'state': state, 'user': user,
                                                       'message': message})

def save_contact_info(request):
    data = request.POST

    try:
        email = data['email']
        validate_email(email)

        name = data['name']
        subject = data['subject']
        description = data['description']

        messageModel.objects.create(name=name, email=email, subject=subject, description=description)
        messages.success(request, 'Your message has been submitted. Thank you')
        return redirect('contact')

    except:
        messages.warning(request, 'Email is not valid')
        return contact(request, data)

