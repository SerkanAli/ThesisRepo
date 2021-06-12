from elg import Service
from elg import Pipeline
from elg.model import *

def AudioToText():
    lt = Service.from_id(489, scope="offline_access")
    result = lt("ServiceAT/AudioFiles/test.mp3")
    print(result)


def TextToSpeech():
    lt = Service.from_id(4837, scope="offline_access")
    result = lt("My name is Kevin, How are you?")
    result.to_file("testfile.mp3")

def TextToText():
    lt = Service.from_id(624, scope="offline_access")
    result = lt('In his new book, Fulfillment, Alec MacGillis writes of an Amazon distribution center in Sparrows Point, Maryland that sits on land once occupied by a Bethlehem Steel plant. MacGillis tells the story of some workers')
    print(result)

def PipelineTest():
    pipeline = Pipeline.from_ids([478, 624], scope="offline_access")
    TEXT_TO_SUMMARIZE = '''In his new book, Fulfillment, Alec MacGillis writes of an Amazon distribution center in Sparrows Point, Maryland that sits on land once occupied by a Bethlehem Steel plant. The story underscores how dramatically the U.S. economy has transformed in recent years. Instead of making things, many of our biggest companies now distribute things made elsewhere. We've moved from an economy of production to one of dispersion. The shift from factory to fulfillment work is core to the American story right now. For the American worker, a factory job like one at Bethlehem Steel was dangerous, but it paid $30 to $40 per hour, and many stuck with it for life. At an Amazon Fulfillment Center, pay starts at $15 per hour, algorithms monitor your performance, and many workers leave soon after joining. "There's 100% turnover in the warehouses," MacGillis told me this week. "100% \every single year." Some blame the move to fulfillment work entirely on Amazon, but it didn't happen in a vacuum. American politicians helped it along by signing trade deals like NAFTA and enthusiastically welcoming China into the World Trade Organization - and doing so without sufficient safeguards. American industry then suffered the consequences, and Amazon reaped the benefits. Listen to Alec MacGillis on this week's Big Technology Podcast on Apple, Spotify, or your app of choice. The U.S. embrace of globalization flooded the country's markets with inexpensive products, and plants stateside couldn't keep up. As American factories went under or moved overseas, there was glaring a need for a company that could get the new, affordable products to Americans' doorsteps. Amazon eagerly stepped in. And its timing couldn't have been better. In January 1994, NAFTA opened up trade between U.S., Canada, and Mexico. Seven months later, Jeff Bezos founded Amazon. In 2000, Amazon launched its third-party marketplace. One year later, China joined the WTO.For workers, going from $40 to $15 per hour meant moving from an annual salary of $80,000 to one closer to $30,000. And as U.S. industry struggled, Amazon's hired 1,400 workers per day. Many American workers are now removed from the production process - employed by middlemen taking a cut - so the drop in wage is natural. MacGillis tells the story of some workers who, on the same land, worked for Bethlehem Steel and then Amazon for one-third the wage. American workers have thus taken a hard look at our political system and found it wanting. In the aftermath of the trade deals, they've been left too often to decide between unemployment and jobs at fulfillment centers, ride-hailing services, and app-based food delivery. In 2016, many workers remembered Bill Clinton signing NAFTA and backing China's entry to the WTO, and voted for Donald Trump. In 2020, as Covid raged, enough moved to Joe Biden's camp that he won the election with an amalgamation of workers and college-educated liberals, what MacGillis calls the "Amazon Coalition." In some cases, Amazon workers drawn to the Democratic party for its alliance with labor were peeing in bottles as they delivered packages to urban-dwellers drawn to the party for its social values. The underlying tension flared up recently as workers at an Amazon fulfillment center in Bessemer, Alabama pushed to unionize. Bernie Sanders and Elizabeth Warren came out strongly in support of the union, fully aware of how vital fulfillment workers are to their future. Amazon then mocked the government for failing the working class. Its executive overseeing the fulfillment centers, Dave Clark, said "We actually deliver a progressive workplace," while hailing Amazon's $15 minimum wage compared to the federal government's $7.25. The union effort in Bessemer seems en route to defeat. But even in victory, it would not have replaced the fulfillment center work with factory work. The reality facing U.S. workers today is that low-paying fulfillment jobs are often their best option. And we're likely to see more political instability if we don't find some way to generate jobs that give workers a shot at the middle class. '''

    results = pipeline(TEXT_TO_SUMMARIZE,output_funcs=[
                lambda x: " ".join([data.features["prefLabel"] for data in x.annotations["Main sentence"]]),
                lambda x: x.texts[0].content,
            ]
        )
    print("German summary: ", results[-1])

def ObjectTest():
    service = Service.from_id(478, scope="offline_access")
    response = service(TextRequest(content="Nikolas Tesla lives in Berlin. MacGillis tells the story of some workers."))  
    for data in response.annotations["Main sentence"]:
        print(data)

    #print("Role:" + response.role)
    print(response.get_content())
    #print("Texts:" + response.texts)
    #print(":" + response.role)
    #print(":" + response.role)
    #print(":" + response.role)
    print(response.auto_content())





#AudioToText()
#TextToText()
#TextToSpeech()

#PipelineTest()
ObjectTest()