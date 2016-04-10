{
    TableName : "Tempreture",
    KeySchema: [       
        { AttributeName: "Termometr", KeyType: "HASH" },  //Partition key
        { AttributeName: "GetDate", KeyType: "RANGE" }  //Sort key
    ],
    AttributeDefinitions: [       
        { AttributeName: "Termometr", AttributeType: "S" },
        { AttributeName: "GetDate", AttributeType: "S" },
	{ AttributeName: 'Val', AttributeType: "N" }
    ],
    ProvisionedThroughput: {       
        ReadCapacityUnits: 10, 
        WriteCapacityUnits: 10
    }
};
