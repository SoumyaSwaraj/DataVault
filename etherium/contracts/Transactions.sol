pragma solidity ^0.5.0;

contract Transactions {
  uint public transCount = 0;

  struct Task {
    uint transid;
    string transdata;
    string transbuyerid;
    string transsellerid;
    string transtimestamp;
    bool completed;
  }

  mapping(uint => Task) public tasks;

  event TaskCreated(
    uint transid,
    string transdata,
    string transbuyerid,
    string transsellerid,
    string transtimestamp,
    bool completed
  );

  event TaskCompleted(
    uint transid,
    bool completed
  );

  constructor() public {
    createTask("DevX Transactions ETH-Blockchain");
  }

  function createTask(string memory _transdata, string memory _transbuyerid, string memory _transsellerid, string memory _transtimestamp) public {
    transCount ++;
    tasks[taskCount] = Task(taskCount, _transdata, _transbuyerid, _transsellerid, _transtimestamp, false);
    emit TaskCreated(taskCount, _transdata, _transbuyerid, _transsellerid, _transtimestamp, false);
  }

  function toggleCompleted(uint _id) public {
    Task memory _task = tasks[_id];
    _task.completed = !_task.completed;
    tasks[_id] = _task;
    emit TaskCompleted(_id, _task.completed);
  }

}
