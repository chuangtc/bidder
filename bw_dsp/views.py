from django.http import HttpResponse
from django.shortcuts import render

from . import bid_request_pb2

from .models import ad_settings

import random, json

# Create your views here.
def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World! It's Bridgewell's assignment </h1>"
                        "<a href='http://bridgewell.chuangtc.com/bw_dsp'>http://bridgewell.chuangtc.com/bw_dsp</a>")

def bidding_strategy_view(request, *args, **kwargs):
    bid_request = request.body
    #print(bid_request)

    #bid_request_msg = bid_request_pb2.BidRequest()
    #ERROR: google.protobuf.message.DecodeError: Wrong wire type in tag.
    #bid_request_msg.ParseFromString(bid_request)
    #print(bid_request_msg)

    bid_request_str=bid_request.decode('utf-8')
    string_id_beg = bid_request_str.index("string id")
    string_id = bid_request_str[string_id_beg:string_id_beg + 20]
    string_id = (string_id[string_id.index("=")+1:string_id.index(";")])

    repeated_Imp_imp_beg = bid_request_str.index("repeated Imp imp")
    repeated_Imp_imp = bid_request_str[repeated_Imp_imp_beg:repeated_Imp_imp_beg + 25]
    repeated_Imp_imp = (repeated_Imp_imp[repeated_Imp_imp.index("=")+1:repeated_Imp_imp.index(";")])

    double_bidfloor_beg = bid_request_str.index("double bidfloor")
    double_bidfloor = bid_request_str[double_bidfloor_beg:double_bidfloor_beg + 25]
    double_bidfloor = (double_bidfloor[double_bidfloor.index("=")+1:double_bidfloor.index(";")])

    bid_floor = float(double_bidfloor)

    queryset = ad_settings.objects.all()
    max_creative_id = -1
    max_bid_price = -100

    for each in queryset:
        if each.status == False:
            continue
        bid_price = each.bidding_cpm * random.randrange(1, 10)
        if bid_price > max_bid_price:
            max_bid_price = bid_price
            max_creative_id = each.creative_id


    # Case :　Return HTTP 204 (No Content) if final bid price less than bid floor　
    if max_bid_price < bid_floor:
        response = HttpResponse()
        response.status_code = 204
        return response

    message_BidResponse = ('message BidResponse { \n',
                           '  string id = '+ string_id+';\n' ,
                           '  repeated Bid bid = '+repeated_Imp_imp+';\n',
                           '  message Bid {\n',
                           '    string id = '+ string_id+';\n',
                           '    string impid = '+str(max_creative_id)+';\n',
                           '    double price = '+str(max_bid_price)+';\n',
                           '  }\n',
                           '}\n'
                           )
    #obj = { "creative_id": max_creative_id, "bid_price": max_bid_price }
    return HttpResponse(message_BidResponse, content_type="text/plain")