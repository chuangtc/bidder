from django.http import HttpResponse
from django.shortcuts import render

from google.protobuf import text_format

from .models import ad_settings

# Create your views here.
def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World! It's Bridgewell's assignment </h1>"
                        "<a href='http://127.0.0.1:8000/bw_dsp'>Location</a>")

def bidding_strategy_view(request, *args, **kwargs):
    bid_request = request.body

    #message = text_format.Parse(bid_request, my_proto_pb2.MyMessage())

    #my_proto_pb2.MyMessage(foo=’bar’)
    #text_proto = text_format.MessageToString(message)

    queryset = ad_settings.objects.all()
    for each in queryset:
        print(each.creative_id)
        print(each.status)
        print(each.bidding_cpm)
        print(each.bid_quantity)

    # Case ３ :　Return HTTP 204 (No Content) if final bid price less than bid floor　
    response = HttpResponse()
    response.status_code = 204
    return response
    #return HttpResponse(bid_request)