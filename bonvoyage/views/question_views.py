from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from ..forms import QuestionForm
from django.utils import timezone
from django.core.checks import messages
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    """
    질문 등록
    """
    if request.method =='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('bonvoyage:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'bonvoyage/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages(request, "수정권한이 없습니다.")
        return redirect('bonvoyage:detail', question_id=question.id)
    
    if request.method =='POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('bonvoyage:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'bonvoyage/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages(request, "삭제권한이 없습니다.")
        return redirect('bonvoyage:detail', question_id=question.id)
    question.delete()
    return redirect('bonvoyage:index')