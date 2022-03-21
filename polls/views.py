from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

# def index(request):
#     latest_questions_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_questions_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/details.html', {'question': q})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def jsonView(request, question_id):
    # q = Question.objects.get(pk=question_id)
    q = get_object_or_404(Question, pk=question_id)
    return JsonResponse({
        'question_text': q.question_text,
        'choices': [{
            'choice_text': c.choice_text,
            'votes': c.votes
            } for c in q.choice_set.all()],
    })

def jsonIndex(request):
    q = Question.objects.all()
    response = {}
    for idx, question in enumerate(q):
        response[idx] = {
            'question_text': question.question_text,
            'choices': [{
                'choice_text': c.choice_text,
                'votes': c.votes,
            } for c in question.choice_set.all()]
        }

    return JsonResponse(response)



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'


# class ResultsView(generic.DetailView):
    # model = Question
    # template_name = 'polls/results.html'