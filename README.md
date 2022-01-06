## [ FSK ADRESAR ] practice REST API

A simple REST API for practicing communication with an API. You can also access this page from the API, by making a GET request to `/api/v1/docs`.

## How to use

### Getting the list of students

To get the list of students, make a GET request to `/api/v1/students`.

Response format:

```json
[
  {
    "firstName": "Ibro",
    "lastName": "Ibric",
    "studentId": "1022",
    "department": "KiT",
    "cycle": 1,
    "semester": 4
  },
  {
    "firstName": "Samir",
    "lastName": "Samirovic",
    "studentId": "1021/II",
    "department": "KT",
    "cycle": 2,
    "semester": 2
  },
  {
    "firstName": "Hasan",
    "lastName": "Hasanovic",
    "studentId": "900/II",
    "department": "PT",
    "cycle": 2,
    "semester": 3
  }
]
```

### Getting single student by ID

In order to fetch data for a single student, make a GET request to `/api/v1/student/student-id`, where `student-id` is the ID of the student you want to fetch. Keep in mind that, if you are fetching by a student ID which has slashes in it (eg. 1000/II) you have to replace `/` with `-`. Therefore, to fetch student with Student ID 902/II, send a request to `/api/v1/student/902-II`. The response is:

```json
{
"studentId": "902/II",
"firstName": "Hasan",
"lastName": "Hasanovic",
"department": "KiT",
"cycle": 2,
"semester": 3
}
```

### Writing data

In order to write the data, make a POST request to `/api/v1/students` and send the following body:

```json
{
  "studentId": "900/II", //string
  "firstName": "Hasan", //string
  "lastName": "Hasanovic", //string
  "department": "PT", //string
  "cycle": 2, //int
  "semester": 3 //integer
}
```

All fields are required and there's type validation for each of these fields. Also, the body should be sent with the parameters ordered exactly as stated above.


### Running with secrets

In order to compile and run the API, as well as use the `create` and `empty` endpoints, you need to create a file `apisecrets.py` and set the following secrets:

```python
ADMIN_CODE = 'your-admin-code'
```

This is just kept as a failsafe, ideally you won't need any of these endpoints.
