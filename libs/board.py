from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from PIL import ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
from .colors import *

clock_fnt = ImageFont.truetype("./static/font/Kodchasan-Bold.ttf", 40)



transport = AIOHTTPTransport(url="https://api.entur.io/journey-planner/v3/graphql")

class Board:
    def __init__(self, query, img):
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.query = gql(query)
        self.img = img
        self.d = ImageDraw.Draw(self.img)

    def draw_board(self):
        self.d.rectangle((0, 0,self.img.width, self.img.height), WHITE)
        self._draw_board(self.client.execute(self.query))

        # draws overlay
        self.d.rounded_rectangle((-50, -50, 165, 74), 50, BLUE)
        self.d.text((15, 10), datetime.now().strftime("%H:%M"), font=clock_fnt, fill=WHITE)


    
    def _draw_board(self, data):
        pass

class DepartureBoard(Board):
    def __init__(self, img, stop_id):
        super().__init__(
            """
            {
                stopPlace(id: "%s") {
                        name
                        estimatedCalls(numberOfDepartures: 5) {
                        cancellation
                        expectedArrivalTime
                        expectedDepartureTime
                        destinationDisplay {
                            frontText
                        }
                        serviceJourney {
                            transportMode
                            line {
                                name
                                transportMode
                                publicCode
                                id
                            }
                        }
                    }
                }
            }
            """ % stop_id, 
            img)
    
    def time_to_departure(self, call):
        departure_time = datetime.fromisoformat(call["expectedDepartureTime"])
        time_now = datetime.now(timezone.utc)
        time_delta = departure_time - time_now
        

        print(departure_time, time_delta)

        return ""


    def _draw_board(self, data):
        line_x = 165/4
        circle_y = 124
        circle_r = 25


        self.d.text((175, 10), data["stopPlace"]["name"], fill=BLACK, font=clock_fnt)
        self.d.line((line_x, circle_y, line_x, 480), BLACK, 10)

        max_line_num_len = 0
        # info loop
        for call in data["stopPlace"]["estimatedCalls"]:
            line_number = call["serviceJourney"]["line"]["publicCode"]
            line_num_len = self.d.textlength(line_number, clock_fnt)

            if line_num_len > max_line_num_len:
                max_line_num_len = line_num_len
        

        # draw loop
        for call in data["stopPlace"]["estimatedCalls"]:
            self.d.circle((line_x, circle_y), circle_r, WHITE, BLACK, 10)

            line_number = call["serviceJourney"]["line"]["publicCode"]
            front_text = call["destinationDisplay"]["frontText"]

            departure_time = self.time_to_departure(call)

            # line
            x0, y0, x1, y1 = line_x + 40, circle_y - 30, line_x + 60 + max_line_num_len, circle_y + 30
            self.d.rounded_rectangle((x0, y0, x1, y1), 15, BLACK)            
            self.d.text(((x0 + x1)/2, (y0 + y1)/2), line_number, WHITE, clock_fnt, anchor="mm")

            # departure time
            x0, x1 = x1 + 20, x1 + 90
            self.d.rounded_rectangle((x0, y0, x1, y1), 15, BLACK) 
            # self.d.text(((x0 + x1)/2, (y0 + y1)/2), departure_time, WHITE, clock_fnt, anchor="mm")

            # front text
            # text_len = self.d.textlength(front_text, clock_fnt)
            # print(text_len, len(front_text))

            # if len(front_text) > 18:
            #     #15
            #     front_text = front_text[:15] + "..."

            # self.d.text((line_x + 300, (y0 + y1)/2), front_text, BLACK, clock_fnt, anchor="lm")

            circle_r = 20
            circle_y += 80
