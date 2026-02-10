from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from PIL import ImageFont, Image
from datetime import datetime, timezone, timedelta
from libs.colors import *
from libs.icons import mode_to_icon
import humanize
import math

from boards.board import Board

_t = humanize.i18n.activate("nb")

header_fnt = ImageFont.truetype("./static/font/Kodchasan-Bold.ttf", 40)
large_fnt = ImageFont.truetype("./static/font/Kodchasan-Regular.ttf", 40)
small_header_fnt = ImageFont.truetype("./static/font/Kodchasan-Bold.ttf", 20)
fnt = ImageFont.truetype("./static/font/Kodchasan-Regular.ttf", 20)

transport = AIOHTTPTransport(url="https://api.entur.io/journey-planner/v3/graphql")

class DepartureBoard(Board):
    def __init__(self, img, stop_id):
        super().__init__(img)
        
        query = """
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
                            publicCode
                        }
                    }
                    transportMode
                }
            }
            """ % stop_id
        
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.query = gql(query)
        self.top_bar_height = 75
    
    def time_to_departure(self, call):
        departure_time = datetime.fromisoformat(call["expectedDepartureTime"])
        time_now = datetime.now(timezone.utc)
        time_delta = departure_time - time_now

        humanized_time = ""

        if time_delta < timedelta(hours=1, minutes=30):
            humanized_time = humanize.naturaldelta(time_delta)
        else:
            humanized_time = departure_time.strftime("%H:%M")

        return humanized_time

    def draw_board(self):
        self.d.rectangle((0, 0,self.img.width, self.img.height), WHITE)

        # draws overlay
        self.d.rectangle((0, 0, 800, self.top_bar_height), BLACK)
        self.d.text((800 - 15, 10), datetime.now().strftime("%H:%M"), font=header_fnt, fill=WHITE, anchor="ra")

        # draw board
        self._draw_board(self.client.execute(self.query))


    def _draw_board(self, data):
        left_padding = 20
        header_height = 35

        self.d.rectangle((0, self.top_bar_height, 800, self.top_bar_height + header_height), WHITE)

        self.d.text((left_padding, self.top_bar_height + 5), "På vei til", fill=BLACK, font=small_header_fnt)
        self.d.text((800 - left_padding, self.top_bar_height + 5), "Avgang", fill=BLACK, font=small_header_fnt, anchor="ra")

        # TODO: hvis ingen er funnet put spørgesmål
        transport_modes = sorted(data["stopPlace"]["transportMode"])
        large_icon_size = 80
        small_icon_size = 40
        if len(transport_modes) <= 2:
            for i, mode in enumerate(transport_modes):
                icon = mode_to_icon(mode, True)
                self.img.paste(icon, (left_padding + (large_icon_size*i), (math.floor((self.top_bar_height - large_icon_size)/2))), icon)
            icon_padding = large_icon_size if len(transport_modes) == 1 else large_icon_size + large_icon_size
        else:
            icon_padding = 0
            icon_x = left_padding
            icon_y = math.floor((self.top_bar_height - large_icon_size)/2)
            for i, mode in enumerate(transport_modes):
                icon = mode_to_icon(mode, False)
                self.img.paste(icon, (icon_x, icon_y), icon)

                if i % 2 == 0:
                    icon_y += small_icon_size
                    icon_padding += small_icon_size
                else:
                    icon_x += small_icon_size
                    icon_y = math.floor((self.top_bar_height - large_icon_size)/2)

                    if i + 2 == len(transport_modes):
                        icon_y += math.floor(small_icon_size/2) - math.floor((self.top_bar_height - large_icon_size)/2)



        # TODO: forkort name hvis for lang
        self.d.text((left_padding*2 + icon_padding, 15), data["stopPlace"]["name"], fill=WHITE, font=header_fnt)

        self.d.line((0, self.top_bar_height + header_height, 800, self.top_bar_height + header_height), BLACK, 3)


        max_line_num_len = 0
        # info loop
        for call in data["stopPlace"]["estimatedCalls"]:
            line_number = call["serviceJourney"]["line"]["publicCode"]
            if call["serviceJourney"]["line"]["transportMode"] == "air":
                line_number = call["serviceJourney"]["publicCode"]
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
            line_num_bg_color, line_num_text_color = mode_to_color(call["serviceJourney"]["line"]["transportMode"])

            self.d.rounded_rectangle((x0, y0, x1, y1), 15, line_num_bg_color) 
            if call["serviceJourney"]["line"]["transportMode"] == "air":
                line_number = call["serviceJourney"]["publicCode"]          
            self.d.text(((x0 + x1)/2, (y0 + y1)/2), line_number, line_num_text_color, header_fnt, anchor="mm")
            
            # front text 
            name_len = self.d.textlength(front_text, header_fnt)
            if name_len > 350:
                #15
                front_text = front_text[:13] + "..."

            self.d.text((x1 + left_padding, (y0 + y1)/2), front_text, BLACK, large_fnt, anchor="lm", stroke_width=5, stroke_fill=WHITE)

            # departure time
            # self.d.rounded_rectangle((x0, y0, x1, y1), 15, BLACK) 
            self.d.text((800 - left_padding, (y0 + y1)/2), departure_time, BLACK, header_fnt, anchor="rm", stroke_width=5, stroke_fill=WHITE)

            y0 += header_height + row_padding
            y1 = y0 + row_height
        
        if len(data["stopPlace"]["estimatedCalls"]) == 0:
            self.d.text((x0, y0), "Ingen servicer funnet...", BLACK, header_fnt, stroke_width=5, stroke_fill=WHITE )

