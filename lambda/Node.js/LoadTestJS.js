//モジュールの読み込み
var aws = require('aws-sdk');
var sqs = new aws.SQS({region: 'ap-northeast-1'});

//sqsのURL
var url = "https://sqs.ap-northeast-1.amazonaws.com/616910136970/Lambda_test";

//メイン処理
exports.handler = function (event, context) {
    // 現在時刻取得
    var date = new Date();
    var now = date.getTime();
    
    var inittime = event.inittime;
    var uuid = event.uuid;
    var seq = event.seq;
    var difftime = now - inittime;
    
    var params = {
        MessageBody: JSON.stringify({"seq": seq, "opentime": now, "inittime": inittime, "uuid": uuid, "difftime":difftime}),
//        MessageBody: JSON.stringify(event),
        QueueUrl: url,
        DelaySeconds: 0
    };
    sqs.sendMessage(params, function (err, data) {
        if (err) {
          console.log(err, err.stack);
        } else {
            console.log(data);
            context.succeed();
        }
    });
};
