
## Wishlist

With this app, a customer can create a wishlist

## Run Locally

Clone the project

```bash
  git clone git@github.com:thaisbighetti/wishlist.git
```

Run Web

```bash
  docker compose up app
```

Run Tests
```bash
  docker compose run tests
```
## API Reference

Use file insomnia/wishlist_insomnia_doc.json to get all endpoints.
#### Customer

```http
  POST /customer/
  data = {"email": "email@email.com", "name": "customer"}
  
  GET/DELETE /customer/{id}
  GET/PATCH /customer/{id}
```

#### Products

```http
  GET/LIST /product/
  GET /product/{id}
```

####  Wishlist
```http
  POST /wishlist/
  data = {"products: ["id1", "id2"]}
  GET /wishlist/
```

#### Token

```http
  POST /token/
  data = {"email":"email@email.com"}
```
