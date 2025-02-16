from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from PIL import ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
from .colors import *
import humanize

_t = humanize.i18n.activate("nb")

header_fnt = ImageFont.truetype("./static/font/Kodchasan-Bold.ttf", 40)
large_fnt = ImageFont.truetype("./static/font/Kodchasan-Regular.ttf", 40)
small_header_fnt = ImageFont.truetype("./static/font/Kodchasan-Bold.ttf", 20)
fnt = ImageFont.truetype("./static/font/Kodchasan-Regular.ttf", 20)


# ferge = blå
# metro = rød
# buss = sort
# trikk = grønn
# tåg = oranjs


transport = AIOHTTPTransport(url="https://api.entur.io/journey-planner/v3/graphql")

class Board:
    def __init__(self, query, img):
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.query = gql(query)
        self.img = img
        self.d = ImageDraw.Draw(self.img)
        self.top_bar_height = 75

    def draw_board(self):
        self.d.rectangle((0, 0,self.img.width, self.img.height), WHITE)

        # draws overlay
        self.d.rectangle((0, 0, 800, self.top_bar_height), BLACK)
        self.d.text((800 - 15, 10), datetime.now().strftime("%H:%M"), font=header_fnt, fill=WHITE, anchor="ra")

        # draw board
        self._draw_board(self.client.execute(self.query))


    
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
                    transportMode
                }
            }
            """ % stop_id, 
            img)
    
    def time_to_departure(self, call):
        departure_time = datetime.fromisoformat(call["expectedDepartureTime"])
        time_now = datetime.now(timezone.utc)
        time_delta = departure_time - time_now

        humanized_time = humanize.naturaldelta(time_delta)
        # if len(humanized_time) > 7:
        #     humanized_time = humanized_time[0:6]


        return humanized_time


    def _draw_board(self, data):
        left_padding = 20
        header_height = 35

        self.d.text((left_padding, self.top_bar_height + 5), "På vei til", fill=BLACK, font=small_header_fnt)
        self.d.text((800 - left_padding, self.top_bar_height + 5), "Avgang", fill=BLACK, font=small_header_fnt, anchor="ra")

        self.d.text((left_padding, 10), data["stopPlace"]["name"], fill=WHITE, font=header_fnt)


        self.d.line((0, self.top_bar_height + header_height, 800, self.top_bar_height + header_height), BLACK, 3)


        max_line_num_len = 0
        # info loop
        for call in data["stopPlace"]["estimatedCalls"]:
            line_number = call["serviceJourney"]["line"]["publicCode"]
            line_num_len = self.d.textlength(line_number, header_fnt)

            if line_num_len > max_line_num_len:
                max_line_num_len = line_num_len
        
        row_height = 60
        row_padding = 35

        x0 = left_padding
        y0 = self.top_bar_height + header_height + row_padding/2 
        x1 = left_padding + 20 + max_line_num_len
        y1 = y0 + row_height

        # draw loop
        for i, call in enumerate(data["stopPlace"]["estimatedCalls"]):

            line_number = call["serviceJourney"]["line"]["publicCode"]
            front_text = call["destinationDisplay"]["frontText"]

            departure_time = self.time_to_departure(call)

            # line
            self.d.rounded_rectangle((x0, y0, x1, y1), 15, BLACK)            
            self.d.text(((x0 + x1)/2, (y0 + y1)/2), line_number, WHITE, header_fnt, anchor="mm")
            
            # front text 
            # maks 350
            name_len = self.d.textlength(front_text, header_fnt)
            print(name_len)

            if name_len > 350:
                #15
                front_text = front_text[:13] + "..."

            self.d.text((x1 + left_padding, (y0 + y1)/2), front_text, BLACK, large_fnt, anchor="lm")

            # departure time
            # self.d.rounded_rectangle((x0, y0, x1, y1), 15, BLACK) 
            self.d.text((800 - left_padding, (y0 + y1)/2), departure_time, BLACK, header_fnt, anchor="rm")

            y0 += header_height + row_padding
            y1 = y0 + row_height


