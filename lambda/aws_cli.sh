
aws lambda invoke \
--invocation-type RequestResponse \
--function-name helloworld \
--region us-west-2 \
--log-type Tail \
--payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' \
--profile adminuser \
outputfile.txt


aws lambda invoke --function-name Lambda_test --region ap-northeast-1 output.txt


for i in 128 256 384 512 640 768 896 1024 1152 1280 1408 1536
do
    aws lambda delete-function --function-name Lambda_test_"$i"M --region ap-northeast-1
    aws lambda create-function --function-name Lambda_test_"$i"M \
    --runtime python2.7 \
    --role arn:aws:iam::616910136970:role/lambda_sqs_execution \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://Lambda_test.zip \
    --region ap-northeast-1 \
    --memory-size "$i" \
    --timeout 300
done


for i in 128 256 384 512 640 768 896 1024 1152 1280 1408 1536
do
    echo Lambda_test_"$i"M
done
