### Start the project

You can start the project as below:

```
docker-compose up --build
```

### Posts apis

I did not implement apis related to posts because the problem was not focusing on that part.

### Auth

In a production project obviously having Authentication and Authorization is an important requirement but here because
of the scope the project I ignored implementing auth and just filled the user_id in api bodies.

### Index and Pagination (Cache)

For better performance I used simple solutions like pagination or database index but obviously with a high loads of
users it does not perform very good so another solution here is using a in memory database as cache.

### Update on write

For not decreasing the performance of our service while users requesting a post review overview(count and average) the
calculation are happening at write time (so the overall calculation time is less because probably read operations are
more and in read we need to aggregate millions of data but in write just need to update one row) and it happens in a
transaction to guarantee atomicity.

## Solutions for `Review Bomb`:

### 1. rate limiting and backoffice approve

(current implementation)
Limiting creation of ratings(it would be better if we enable it on update too) and wait for a backoffice user to approve
the rating. (authentication here is a key principle because certain people from the company can
call `api/rating/approve/<int:post_id>/<int:user_id>`)
Actually it's good to mention that this solution because of the overhead of operation (backoffice approving) and the
tuning of rate limiter (the limit and strategy of rate limiter needs tuning to have a better user experience and
decrease the operational headache) is not a very good solution. (another problem is that users would experience that
their ratings are not appearing in the results to addressing this issue and operational overhead we can just deny new
requests after reaching the limit of rate limit in which we will have new problems such a bad experience for users)

### 2. user reputation

We can use some user reputation or validation mechanism in which we decide if a user is eligible to create a rating in a
specific time (rate limit or n days after registration or ...) or at all. (like `StackOverFlow` that with contributions
and activities you gain reputation, and then you can up-vote or down-vote)

### 3. smooth decreasing (in the case that slope is important)

If it is just the matter of time we apply new ratings smoothly. (in this case instead of using transaction it is better
to use some queue or worker to process after a while e.g. using Celery)