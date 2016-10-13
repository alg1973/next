{
    TableName : "Tempreture",
    KeySchema: [       
        { AttributeName: "Termometr", KeyType: "HASH" },  //Partition key
        { AttributeName: "GetDate", KeyType: "RANGE" }  //Sort key
    ],
    AttributeDefinitions: [       
        { AttributeName: "Termometr", AttributeType: "S" },
        { AttributeName: "GetDate", AttributeType: "N" },
    ],
    ProvisionedThroughput: {       
        ReadCapacityUnits: 10, 
        WriteCapacityUnits: 10
    }
};
{
    TableName : "Commands",
    KeySchema: [       
        { AttributeName: "Termometr", KeyType: "HASH" },  //Partition key
        { AttributeName: "Room", KeyType: "RANGE" }  //Sort key
    ],
    AttributeDefinitions: [       
        { AttributeName: "Termometr", AttributeType: "S" },
        { AttributeName: "Room", AttributeType: "S" },
    ],
    ProvisionedThroughput: {       
        ReadCapacityUnits: 5, 
        WriteCapacityUnits: 5
    }
};
