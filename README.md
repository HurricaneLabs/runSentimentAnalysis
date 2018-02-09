# runSentimentAnalysis
Sentiment Analysis for Closed tickets 

This run in AWS Lambda. You will need to have two environment variables to run this: 
  splServer (the Splunk server you are sending data to, full url with HEC path required) 
  splToken (the Splunk HEC token for sending events into Splunk) 
  
You will also need ticket data in S3 (really any text will do, it doesn't HAVE to be ticket data). The function runs, from left to right: 

   Data is put into S3 --> runSentimentAnaylysis is triggered --> data is sent to AWS Comprehend --> Results are stored in Splunk via HTTP Event Collector. 
   
   
   Enjoy! 
