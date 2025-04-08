from django.http import HttpResponse
from django.shortcuts import render
from parser_app.utils import parse_mebmer, parse_result


# Create your views here.
def parse_members(request):
    try:
        parse_mebmer.get_member()

        return HttpResponse("data parsed and saved succesSful!", status=200)

    except Exception as e:
        return HttpResponse(f"parsing error: {str(e)}", status=500)


def parse_results(request):
    try:
        parse_result.get_results()

        return HttpResponse("data parsed and saved succesSful!", status=200)

    except Exception as e:
        return HttpResponse(f"parsing error: {str(e)}", status=500)
