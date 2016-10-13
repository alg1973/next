{
    TableName : "Tempreture",
    KeySchema: [       
        { AttributeName: "Thermometr", KeyType: "HASH" },  //Partition key
        { AttributeName: "GetDate", KeyType: "RANGE" }  //Sort key
    ],
    AttributeDefinitions: [       
        { AttributeName: "Thermometr", AttributeType: "S" },
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
        { AttributeName: "Thermometr", KeyType: "HASH" },  //Partition key
        { AttributeName: "Boiler", KeyType: "RANGE" }  //Sort key
    ],
    AttributeDefinitions: [       
        { AttributeName: "Thermometr", AttributeType: "S" },
        { AttributeName: "Boiler", AttributeType: "S" },
    ],
    ProvisionedThroughput: {       
        ReadCapacityUnits: 5, 
        WriteCapacityUnits: 5
    }
};
