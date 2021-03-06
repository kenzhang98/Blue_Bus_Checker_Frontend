# -*- coding: utf-8 -*-

import logging
import requests as req  

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = "Blue Bus Checker"
WELCOME_MESSAGE = "Which bus information would you like to know?"
HELP_MESSAGE = "You can say when is the next bus for Bursley Inbound, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Blue Bus Checker Skill can't help you with that.  It can help you track the buses and plan your commute ahead of time"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Built-in Intent Handlers
class GetBusStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("GetBusStopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetBusStopIntentHandler")

        speech = "in GetBusStopIntentHandler"

        inputName = str(handler_input.request_envelope.request.intent.slots["busStop"].value)
        outputName = ""

        print("inputName: " + inputName)

        if(inputName == "Baits 1".lower()):
            outputName = "Baits I"
        elif(inputName.lower() == "Baits 2 Inbound".lower()):
            outputName = "Baits II Inbound"
        elif(inputName.lower() == "Bursley Inbound".lower()):
            outputName = "Bursley Hall Inbound"
        elif(inputName.lower() == "Pierpont inbound".lower()):
            outputName = "Pierpont Commons, Murfin Inbound"
        elif(inputName.lower() == "Mitchell field".lower()):
            outputName = "Fuller Rd at Lot NC-78, Mitchell Field (1)"
        elif(inputName.lower() == "glen inbound".lower()):
            outputName = "Glen Inbound"
        elif(inputName.lower() == "Rackham".lower()):
            outputName = "Rackham Bldg"
        elif(inputName.lower() == "CCTC".lower()):
            outputName = "Central Campus Transit Center: Chemistry"
        elif(inputName.lower() == "Stockwell".lower()):
            outputName = "Stockwell Hall Outbound"
        elif(inputName.lower() == "Cardiovascular Center".lower()):
            outputName = "Cardiovascular Center"
        elif(inputName.lower() == "Zina Pitcher".lower()):
            outputName = "Zina Pitcher"
        elif(inputName.lower() == "glen outbound".lower()):
            outputName = "Glen/Catherine Outbound"
        elif(inputName.lower() == "fuller road".lower()):
            outputName = "Fuller Rd at Mitchell Field, Lot M-75"
        elif(inputName.lower() == "pierpont outbound".lower()):
            outputName = "Pierpont Commons, Murfin Outbound"
        elif(inputName.lower() == "Bursley Outbound".lower()):
            outputName = "Bursley Hall Outbound"
        elif(inputName.lower() == "Baits 2 outbound".lower()):
            outputName = "Baits II Outbound"
        else:
            response = "I dont understand the stop name."
            handler_input.response_builder.speak(response).set_should_end_session(True)

        outputName = "+".join(outputName.split())
        api_request = "https://v6lr81x979.execute-api.us-east-1.amazonaws.com/api/" + outputName
        api_response = req.get(api_request).json()
        can_catch = str(api_response["can_catch"])
        time_to_walk = str(api_response["time_to_walk"])
        next_bus_time = api_response["next_bus_time"]

        if(can_catch == "True"):
            response = "The next bus is arriving at " + str(next_bus_time[0]) + " " + str(next_bus_time[1]) + ". The walk to the bus stop will take about " + str(time_to_walk) + " minutes."
        else:
            response = "You are going to miss the next bus. The first bus that you can catch will come at " + str(next_bus_time[0]) + " " + str(next_bus_time[1]) + ". The walk to the bus stop will take about " + str(time_to_walk) + " minutes."

        handler_input.response_builder.speak(response).set_should_end_session(True)
        
        return handler_input.response_builder.response

class LaunchIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        logger.info("In LaunchIntentHandler")

        speech = WELCOME_MESSAGE
        random_fact = "testing"

        deviceid = str(handler_input.request_envelope.context.system.device.device_id)

        print(deviceid)

        handler_input.response_builder.speak(speech).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, random_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetBusStopIntentHandler())
sb.add_request_handler(LaunchIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
