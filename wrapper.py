from conference_spider import Schedule
import json
import copy


def get_dummy_dict():
    dummy_dict = {"conference": {
        "name": "NAACL 2019",
        "location": "Frankfurt",
        "datetime": "4. - 10. May",
        "submission_deadlines": ["10. February", "11. February"],
        "topics": ["NLP", "Transformers"],
        "organizers": ["orga1", "orga2"],
        "papers": [
            {
                "authors": ["1", "2"],
                "title": "titel",
                "link": "http"
            },
            {
                "authors": ["1", "2"],
                "title": "titel",
                "link": "http"
            }
        ],
        "tutorials": [
            {
                "title": "titel",
                "authors": ["1", "2"],
                "abstract": "abstract of this tutorial",
                "datetime": "2019-10-03 14:00-15:00",
                "location": "room number",
                "link": "http"
            }
        ],
        "keynotes": [
            {
                "title": "titel",
                "authors": ["1", "2"],
                "abstract": "abstract of the keynote",
                "datetime": "2019-10-03 14:00-15:00",
                "location": "room number",
                "link": "http"
            }
        ],
        "workshops": [
            {
                "title": "titel",
                "authors": ["1", "2"],
                "abstract": "abstract of the workshop",
                "datetime": "2019-10-03 14:00-15:00",
                "location": "room number",
                "link": "http"
            }
        ]
    }
    }
    return dummy_dict


def add_keynotes_to_dummy(dictionary, information):
    keynote_item = {
        "title": "titel",
        "authors": ["1", "2"],
        "abstract": "abstract of the keynote",
        "datetime": "2019-10-03 14:00-15:00",
        "location": "room number",
        "link": "http"
    }
    dictionary["conference"]['keynotes'].clear()

    for i in range(0, len(information[0])):
        # print(dictionary["conference"]['keynotes'])
        keynote_item['title'] = information[0][i]
        keynote_item['datetime'] = information[1][i] + " " + information[2][i]
        keynote_item['authors'] = information[4][i]
        keynote_item['location'] = information[3][i]
        dictionary["conference"]['keynotes'].append(copy.copy(keynote_item))
    return dictionary


def add_papers_to_dummy(dictionary, information, information_author):
    paper_item = {
                "authors": ["1", "2"],
                "title": "titel",
                "link": "http"
            }
    dictionary["conference"]['papers'].clear()

    for i in range(0, len(information[0])):
        # print(dictionary["conference"]['keynotes'])
        paper_item['title'] = information[i]
        paper_item['authors'] = information_author[i]
        dictionary["conference"]['papers'].append(copy.copy(paper_item))
    return dictionary


def add_workshops_to_dummy():
    # TODO search and add all tutorials to the json dummy
    return "null"


string = 'C:/Users/Y508854/Documents/DSAP NAACL 19 conference/naacl_schedule_2019/data'
my_schedule = Schedule(string)
my_schedule.load_schedule()


keynotes_info = my_schedule.get_keynotes_time_loc('NAACL 19')
all_sessions = my_schedule.get_session_titles('NAACL 19')
paper_info = []
paper_info_authors = []
for session in all_sessions:
    paper_info.append(my_schedule.get_session_talks(session))
    paper_info_authors.append(my_schedule.get_session_speakers(session))

my_dict = get_dummy_dict()
add_keynotes_to_dummy(my_dict, keynotes_info)
add_papers_to_dummy(my_dict, [item for sublist in paper_info for item in sublist],
                    [item for sublist in paper_info_authors for item in sublist])

with open("file.json", 'w') as f:
    json.dump(my_dict, f)

