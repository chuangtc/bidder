# Bidding server

A bidding server acts as a buyer in Real-Time Bidding. When there's an ad slot available for selling in the market, bidding server will receive a bid request. It should then choose an ad from its inventory, determine a bid price, and return the bid result to the seller.

You are required to implement a bidding server according to spec, and demonstrate your implementation's correctness and performance.

## Guideline

Follow these guidelines as much as you can:

* Your codebase should be at production level (for you to interpret what this means).
* Your codebase should be easy to introduce future specs.
* Your codebase should be easily understandable for other developers.

## Specs
  
1. Endpoint should be `http://<your_domain>/bw_dsp`  

2. Prepare a relational database as the data source of your bidding server.

**Database name**  : `dsp_rtb`  

**Table name** : `ad_settings`  

**The ad setting table schema**   

| Column name | Type | Comment |
|----------|:-------------:|:------|
| creative_id | int | ID of advertising creative |
| status | bool | Is capable of being bid  |
| bidding_cpm | int | Cost per 1000 impression |
| bid_quantity | int | The maximum number of bid count |

**testing data**   

| creative_id | status | bidding_cpm | bid_quantity |
|----------|:-------------:|------:|------:|
| 1 |  true | 5 | 10000 |
| 2 |  false | 5 | 10000 |
| 3 |  true | 7 | 30000 |
| 4 |  true | 2 | 50000 |
| 5 |  true | 9 | 100000 |

3. Use protocol buffers (`syntax = "proto3"`) to receive requests and send response.
    ```
	message BidRequest {
	  // Unique ID of the bid request, provided by the exchange.
	  string id = 1;

	  //Array of impression objects.
	  //Multiple impression auctions may be specified in a single bid
	  //request. At least one impression is required for a valid bid request.
	  repeated Imp imp = 2;

		message Imp {
		  // A unique identifier for this impression within the context of
		  // the bid request (typically, value starts with 1,
		  // and increments up to n for n impressions).
		  string id = 1;

		  // Bid floor for this impression (in CPM of bidfloorcur).
		  // value : [0, 20]
		  double bidfloor = 2;
		}

	  User user = 3;
		  message User {
		  // Unique consumer ID of this user on the exchange.
		  string id = 1;

		  // Buyer's user ID for this user as mapped by exchange for the buyer.
		  string buyeruid = 2;
		}
	}
    ```

	```
	message BidResponse {
	  // ID of the bid request to which this is a response.
	  string id = 1;

	  // Array of 1+ Bid objects each related to an
	  // impression. Multiple bids can relate to the same impression.
	  repeated Bid bid = 2;

		message Bid {
		  //ID for the bid object chosen by the
		  //bidder for tracking and debugging purposes. Useful when multiple bids
		  //are submitted for a single impression for a given seat.
		  string id = 1;

		  //ID of the impression object to which
		  //this bid applies
		  string impid = 2;

		  // bid price in CPM
		  double price = 3;
		}
	}
    ```

4. Use the bidding strategy described below to bid and send response.
  
   (1) Bid price = bidding_cpm * (random int between 1 and 10)
   (2) Choose the creative with largest bid price  
   (3) Return HTTP 204 (No Content) if final bid price less than bid floor  
   (4) Do not choose creatives with status=false
   (5) Stop using creatives of which bid count has exceeded bid_quantity. i.e. You can at most bid with the creative bid_quantity times.