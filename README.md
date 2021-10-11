# Businese Card scanner

recognize business card, support language: T.Chinese, S.Chinese, English

# 1. Installation Guide

## 1.1 Requirements

- Python 3.7.x

## 1.2 Docker

Run application using docker

    docker build -t businesscardocrimage .

    docker run -d --name businessCardOCRContainer -p 8080:80 -e MODULE_NAME="application" businesscardocrimage

After building, access API via [http://localhost:8080/docs](http://localhost:8080/docs)

---

# 2. API

## Recognise business card

### Endpoint

    /recognise

### Request Method

    POST

### Parameters

JSON body

| Name | Type | Desc                                                 |
| ---- | ---- | ---------------------------------------------------- |
| file | file | File Upload, supported type: `.jpeg`, `.jpg`, `.png` |

### Response

Success

```json
{
  "success": True,
  "message": "",
  "data": [
    {
      "Name": "Chan Tai Man",
      "last_name": "Chan",
      "first_name": "Tai Man",
      "contact_number": [
        '37097008'
      ],
      "address": [
        "Room 2663, HKUST, Clear Water Bay, Hong Kong"
      ],
      "email": [
        "example@gmail.com"
      ]
    }
  ]
}
```

Fail

```json
{
  "success": False,
  "message": "Error message",
  "data": []
}
```

---
