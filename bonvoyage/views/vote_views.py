from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.checks import messages

from ..models import Question, Answer


@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
    질문 추천
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request,"본인이 작성한 글은 추천할 수 없습니다ㅎ")
    else:
        question.voter.add(request.user)
    return redirect('bonvoyage:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    답글 추천
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request,"본인이 작성한 글은 추천할 수 없습니다ㅎ")
    else:
        answer.voter.add(request.user)
    return redirect('bonvoyage:detail', answer_id=answer.question.id)