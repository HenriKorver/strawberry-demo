import copy

book_data= [
    {
        "id": 1,
        "title": "De Aanslag",
        "publish_date": None
        "authors": [1]
    },
    {
        "id": 2,
        "title": "De Donkere Kamer van Damocles",
        "publish_date": None
        "authors": [2]
    },
    {
        "id": 3,
        "title": "Nooit meer slapen",
        "publish_date": None
        "authors": [2]
    },
    {
        "id": 4,
        "title": "Theorie van het schaakspel: Het middenspel 1",
        "publish_date": None
        "authors": [3,4]
    }
]

author_data= [
    {
        "id": 1,
        "name": "Harry Mulisch",
    },
    {
        "id": 2,
        "name": "Willem Frederik Hermans",
    },
    {
        "id": 3,
        "name": "M. Euwe",
    },
    {
        "id": 4,
        "name": "H. Kramer",
    }
]

book_data_backup = copy.deepcopy(book_data)
author_data_backup = copy.deepcopy(author_data)