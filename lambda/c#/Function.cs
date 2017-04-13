using Amazon.Lambda.Core;
using Amazon.S3;
using Amazon.S3.Transfer;
using System;

//[assembly:LambdaSerializer(typeof(Amazon.Lambda.Serialization.Json.JsonSerializer))]
namespace AWSLambdaSample
{
        public class Function
        {
		    [LambdaSerializer(typeof(Amazon.Lambda.Serialization.Json.JsonSerializer))]            
            public string FunctionHandler(SampleData sampledata, ILambdaContext context)
            {
			//現在時刻取得（ミリ秒）
			DateTime UNIX_EPOCH = new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc);

			DateTime currenttime = DateTime.Now;
			double opentime = (currenttime.ToUniversalTime() - UNIX_EPOCH).TotalMilliseconds;

			sampledata.opentime = (long)opentime;

			//差分時間
			sampledata.difftime = (long)opentime - sampledata.inittime;


			//ローカルファイル作成
			string filename = "/tmp/" + sampledata.seq + sampledata.uuid + ".txt";

			System.Text.Encoding enc = new System.Text.UTF8Encoding();
			System.IO.File.WriteAllText(filename, sampledata.ToString(), enc);


			//s3 upload
			string bucketName = "lambda-load-test";
			string uploadObjectKey = sampledata.seq + sampledata.uuid + ".txt";
			string directoryname = filename;

			TransferUtility fileTransferUtility = new TransferUtility(new AmazonS3Client(Amazon.RegionEndpoint.APNortheast1));
			TransferUtilityUploadRequest request = new TransferUtilityUploadRequest()
			{
				BucketName = bucketName,
				Key = uploadObjectKey,
				FilePath = directoryname
			};

			context.Logger.LogLine(uploadObjectKey);

			fileTransferUtility.Upload(request);


   	/*
			try
			    {

				//インスタンスの作成
				var client = new AmazonSQSClient();
				var request = new SendMessageRequest
				{
					//MessageBody = sampledata.ToString(),
					MessageBody = "Message",
					QueueUrl = "https://sqs.ap-northeast-1.amazonaws.com/618471883049/lambda-load-test-que"
				};
				context.Logger.LogLine("check point1");
				client.SendMessageAsync(request);
				context.Logger.LogLine("check point2");
			    }
			    catch (AmazonSQSException)
			    {
				context.Logger.LogLine("Error");
			    }
			    */
			        //ログ出力
			        context.Logger.LogLine(sampledata.ToString());
			        return sampledata.ToString();

                        
             }
		        
        }


        public class SampleData
	    {
                public long inittime{get; set;}
                public string seq { get; set; }
                public string uuid { get; set; }
		        public long opentime { get; set; }
		        public long difftime { get; set; }
		        override public string ToString()
		        {
			return $"inittime={inittime}, seq={seq}, uuid={uuid}, opentime={opentime}, difftime={difftime}";
		        }
        }
}

