# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Booking, Room, User
from webApi.models import User
from webApi.services import sendMail


@api_view(['POST'])
def addBooking(request):
    fail = {}
    responses = {}
    data = json.loads(request.body.decode('utf-8'))

    if 'roomId' not in data:
        fail['msg'] = "Please provide room id"
        return failure_response(fail)
    elif 'userId' not in data:
        fail['msg'] = "Please provide user id"
        return failure_response(fail)
    elif 'startTime' not in data:
        fail['msg'] = "Please provide start time"
        return failure_response(fail)
    elif 'endTime' not in data:
        fail['msg'] = "Please provide end time"
        return failure_response(fail)
    elif 'bookingDate' not in data:
        fail['msg'] = "Please provide booking date"
        return failure_response(fail)
    elif 'agenda' not in data:
        fail['msg'] = "Please provide agenda"
        return failure_response(fail)

    booking = Booking()
    booking.roomId = Room.objects.get(roomId=data['roomId'])
    booking.userId = User.objects.get(userId=data['userId'])
    booking.startTime = data['startTime']
    booking.endTime = data['endTime']
    booking.agenda = data['agenda']
    booking.historyState = 0
    booking.save()
    responses["status"] = "Room Added Successfully"
    return success_response(responses)

# def isBookingAllowed():
#     fail = {}
#     responses = {}
#     data = json.loads(request.body.decode('utf-8'))
#     roomBookings = Bookings.objects.filter(roomId__exact=roomId).filter(endTime__lt=data.startTime).
#     if isUserAuthorized(userId):
#         for index in roomBookings:
#             if data.startTime <


@api_view(['GET'])
def userAuthorizedForBooking(request):
    responses = {
        "msg": "!Success"
    }
    fail = {}
    userId = request.GET['userId']
    user = User.objects.get(userId=userId)

    history = Booking.objects.filter(
        userId=userId).values('historyState')

    if user.role > 2:
        fail['msg'] = "Can't book the room"
        return failure_response(fail)

    for index in history:
        if index["historyState"] == 1:
            fail['msg'] = "Please provide MoM for previous booking"
            return failure_response(fail)
    return success_response(responses)


@api_view(['GET'])
def getBookings(request, *args, **kwargs):
    fail = {}
    try:
        bookings = Booking.objects.all().values()
        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)


@api_view(['post'])
def getBookingsById(request):
    fail = {}
    try:
        userId = request.GET['userId']
        bookings = Booking.objects.filter(userId=userId)
        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
