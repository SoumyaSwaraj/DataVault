const Transactions = artifacts.require('./Transactions.sol')

contract('Transactions', (accounts) => {
  before(async () => {
    this.transactions = await Transactions.deployed()
  })

  it('deploys successfully', async () => {
    const address = await this.transactions.address
    assert.notEqual(address, 0x0)
    assert.notEqual(address, '')
    assert.notEqual(address, null)
    assert.notEqual(address, undefined)
  })

  it('lists Transactions', async () => {
    const transCount = await this.transactions.taskCount()
    const task = await this.transactions.tasks(transCount)
    assert.equal(task.transid.toNumber(), transCount.toNumber())
    assert.equal(task.transdata, 'DevX Transactions ETH-Blockchain')
    assert.equal(task.completed, false)
    assert.equal(transCount.toNumber(), 1)
  })

  it('creates Transactions', async () => {
    const result = await this.transactions.createTask('A new task')
    const transCount = await this.transactions.taskCount()
    assert.equal(transCount, 2)
    const event = result.logs[0].args
    assert.equal(event.transid.toNumber(), 2)
    assert.equal(event.transdata, 'A new task')
    assert.equal(event.completed, false)
  })

})
