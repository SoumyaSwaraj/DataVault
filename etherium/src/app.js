App = {
  loading: false,
  contracts: {},

  load: async () => {
    await App.loadWeb3()
    await App.loadAccount()
    await App.loadContract()
    await App.render()
  },

  // https://medium.com/metamask/https-medium-com-metamask-breaking-change-injecting-web3-7722797916a8
  loadWeb3: async () => {
    if (typeof web3 !== 'undefined') {
      App.web3Provider = web3.currentProvider
      web3 = new Web3(web3.currentProvider)
    } else {
      window.alert("Please connect to Metamask.")
    }
    // Modern dapp browsers...
    if (window.ethereum) {
      window.web3 = new Web3(ethereum)
      try {
        // Request account access if needed
        await ethereum.enable()
        // Acccounts now exposed
        web3.eth.sendTransaction({/* ... */})
      } catch (error) {
        // User denied account access...
      }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
      App.web3Provider = web3.currentProvider
      window.web3 = new Web3(web3.currentProvider)
      // Acccounts always exposed
      web3.eth.sendTransaction({/* ... */})
    }
    // Non-dapp browsers...
    else {
      console.log('Non-Ethereum browser detected. You should consider trying MetaMask!')
    }
  },

  loadAccount: async () => {
    // Set the current blockchain account
    App.account = web3.eth.accounts[0]
  },

  loadContract: async () => {
    // Create a JavaScript version of the smart contract
    const transactions = await $.getJSON('transactions.json')
    App.contracts.transactions = TruffleContract(transactions)
    App.contracts.transactions.setProvider(App.web3Provider)

    // Hydrate the smart contract with values from the blockchain
    App.transactions = await App.contracts.transactions.deployed()
  },

  render: async () => {
    // Prevent double render
    if (App.loading) {
      return
    }

    // Update app loading state
    App.setLoading(true)

    // Render Account
    $('#account').html(App.account)

    // Render Tasks
    await App.renderTasks()

    // Update loading state
    App.setLoading(false)
  },

  renderTasks: async () => {
    // Load the total task count from the blockchain
    const transCount = await App.transactions.transCount()
    const $taskTemplate = $('.taskTemplate')

    // Render out each task with a new task template
    for (var i = 1; i <= transCount; i++) {
      // Fetch the task data from the blockchain
      const task = await App.transactions.tasks(i)
      const transId = task[0].toNumber()
      const transData = task[1]
      const transBuyerId = task[2]
      const transSellerId = task[3]
      const transTimeStamp = Date.now();

      // Create the html for the task
      const $newTransTemplate = $taskTemplate.clone()
      $newTransTemplate.find('.transid').html(transId)
      $newTransTemplate.find('.content').html(transData)
      $newTransTemplate.find('.buyer').html(transBuyerId)
      $newTransTemplate.find('.seller').html(transSellerId)
      $newTransTemplate.find('.timestamp').html(transTimeStamp)
      

      // Put the task in the correct list
      if (taskCompleted) {
        $('#completedTaskList').append($newTransTemplate)
      } else {
        $('#taskList').append($newTransTemplate)
      }

      // Show the task
      $newTransTemplate.show()
    }
  },

  createTask: async () => {
    App.setLoading(true)
    const content = $('#newTask').val()
    await App.transactions.createTask(content)
    window.location.reload()
  },

  toggleCompleted: async (e) => {
    App.setLoading(true)
    const taskId = e.target.name
    await App.transactions.toggleCompleted(taskId)
    window.location.reload()
  },

  setLoading: (boolean) => {
    App.loading = boolean
    const loader = $('#loader')
    const content = $('#content')
    if (boolean) {
      loader.show()
      content.hide()
    } else {
      loader.hide()
      content.show()
    }
  }
}

$(() => {
  $(window).load(() => {
    App.load()
  })
})
