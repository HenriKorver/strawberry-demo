import copy

book_data= [
    {
        "id": 1,
        "title": "De Aanslag",
        "year": 1982,
        "author_id": 1
    },
    {
        "id": 2,
        "title": "De Donkere Kamer van Damocles",
        "year": 1958,
        "author_id": 2
    },
    {
        "id": 3,
        "title": "Nooit meer slapen",
        "year": 1966,
        "author_id": 2
    },
    {
        "id": 4,
        "title": "Theorie van het schaakspel: Het middenspel 1",
        "year": 1977,
        "author_id": 3
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