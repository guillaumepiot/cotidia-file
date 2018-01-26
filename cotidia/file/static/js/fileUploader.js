'use strict';

(function () {
  function FileUploader (input, headers) {
    // Internal state
    this.queue = {}

    // Useful vars we will use
    this.input = input
    this.parent = input.parentElement
    this.headers = headers

    if (! this.input.dataset.uploadUrl) {
        throw new Error('You must define an upload URL.')
    }

    if (! this.input.dataset.objectId) {
        throw new Error('You must define an object ID.')
    }

    this.uploadUrl = this.input.dataset.uploadUrl
    this.contentType = input.dataset.contentType
    this.objectId = input.dataset.objectId
    this.taxonomy = input.dataset.taxonomy
    this.public = input.dataset.public

    this.decorateInput()
  }

  FileUploader.prototype.decorateInput = function () {
    // Create button to select file(s)
    var newButton = document.createElement('button')
    newButton.type = 'button'
    newButton.classList.add('btn')
    newButton.classList.add('btn--primary')

    if (this.input.multiple) {
      newButton.innerHTML = 'Select files'
    } else {
      newButton.innerHTML = 'Select file'
    }

    newButton.addEventListener('click', this.triggerFileInput.bind(this))

    // Hide original input
    this.input.style.display = 'none'

    this.parent.appendChild(newButton)

    this.uploadContainer = document.createElement('div')
    this.uploadContainer.classList.add('uploader')

    this.parent.appendChild(this.uploadContainer)

    this.input.addEventListener('change', this.handleFiles.bind(this))
  }

  FileUploader.prototype.triggerFileInput = function (e) {
    e.target.blur()

    var ev = document.createEvent('MouseEvents')
    ev.initEvent('click')
    this.input.dispatchEvent(ev)
  }

  FileUploader.prototype.handleFiles = function () {
    var files = this.input.files

    if (files && files.length) {
      for (var i = 0; i < files.length; i++) {
        this.queueFile(files[i])
      }

      this.processNextQueueItem()
    }
  }

  FileUploader.prototype.queueFile = function (file) {
    // Create progress item in HTML and store reference in this.queue
    var upload = document.createElement('div')
    upload.classList.add('upload')

    var message = document.createElement('div')
    message.classList.add('alert')
    message.classList.add('hidden')

    var header = document.createElement('div')
    header.classList.add('upload__header')

    var filename = document.createElement('div')
    filename.classList.add('upload__filename')
    filename.innerHTML = file.name

    var actions = document.createElement('div')
    actions.classList.add('upload__actions')

    var actionsIcon = document.createElement('i')
    actionsIcon.classList.add('upload-action__icon')
    actionsIcon.classList.add('fa')
    actionsIcon.classList.add('fa-fw')

    var progress = document.createElement('div')
    progress.classList.add('upload__progress')
    progress.classList.add('progress')

    var bar = document.createElement('div')
    bar.classList.add('progress__bar')

    actions.appendChild(actionsIcon)

    header.appendChild(filename)
    header.appendChild(actions)

    progress.appendChild(bar)

    upload.appendChild(message)
    upload.appendChild(header)
    upload.appendChild(progress)

    this.uploadContainer.appendChild(upload)

    this.queue[file.name] = {
      dom: {
        upload: upload,
        message: message,
        actions: actions,
        actionsIcon: actionsIcon,
        progress: progress,
        bar: bar,
      },
      file: file,
      state: 'queued',
      percent: 0,
      extra: null,
    }

    this.updateDOM(file)
  }

  FileUploader.prototype.updateDOM = function (file) {
    var item = this.queue[file.name]

    item.dom.upload.classList.remove('upload--queued')
    item.dom.upload.classList.remove('upload--uploading')
    item.dom.upload.classList.remove('upload--complete')
    item.dom.upload.classList.remove('upload--error')
    item.dom.upload.classList.add('upload--' + item.state)

    if (item.state === 'complete') {
      item.dom.actionsIcon.classList.remove('fa-times')
      item.dom.actionsIcon.classList.remove('fa-refresh')
      item.dom.actionsIcon.classList.remove('fa-spin')
      item.dom.actionsIcon.classList.add('fa-check')

      item.dom.message.classList.remove('alert--warning')
      item.dom.message.classList.remove('alert--error')
      item.dom.message.classList.add('alert--success')
    } else if (item.state === 'error') {
      item.dom.actionsIcon.classList.remove('fa-check')
      item.dom.actionsIcon.classList.remove('fa-refresh')
      item.dom.actionsIcon.classList.remove('fa-spin')
      item.dom.actionsIcon.classList.add('fa-times')

      item.dom.message.classList.remove('alert--success')
      item.dom.message.classList.remove('alert--warning')
      item.dom.message.classList.add('alert--error')
    } else {
      item.dom.actionsIcon.classList.remove('fa-times')
      item.dom.actionsIcon.classList.remove('fa-check')
      item.dom.actionsIcon.classList.add('fa-refresh')
      item.dom.actionsIcon.classList.add('fa-spin')

      item.dom.message.classList.remove('alert--success')
      item.dom.message.classList.remove('alert--error')
      item.dom.message.classList.add('alert--warning')

      item.dom.bar.style.width = item.percent + '%'
    }

    if (item.extra) {
      item.dom.message.classList.remove('hidden')
      item.dom.message.innerHTML = item.extra
    } else {
      item.dom.message.classList.add('hidden')
    }
  }

  FileUploader.prototype.updateState = function (file, state, percent, extra) {
      this.queue[file.name].state = state

      if (percent) {
        this.queue[file.name].percent = percent
      }

      if (extra) {
        this.queue[file.name].extra = extra
      }

      this.updateDOM(file)
  }

  FileUploader.prototype.updateProgress = function (file, percent) {
      this.queue[file.name].percent = percent
      this.updateDOM(file)
  }

  FileUploader.prototype.processNextQueueItem = function () {
    // If at least one file is already uploading, we don't need to do anything.
    if (Object.values(this.queue).some(function (item) { return item.state === 'uploading' })) {
      return
    }

    // Pick the next file to upload and process it.
    var file = Object.values(this.queue).find(function (item) { return item.state === 'queued' })

    if (file) {
      this.processFile(file.file)
    }
  }

  FileUploader.prototype.processFile = function (file) {
    this.updateState(file, 'uploading')

    var xhr = new XMLHttpRequest()

    var self = this

    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        self.updateState(file, 'complete', 100)
      } else {
        var extra = 'There was an issue uploading the file.'

        // If it's a 400 response, there's probably some JSON error message data.
        if (xhr.status === 400) {
          try {
            var json = JSON.parse(xhr.responseText)
            extra = json.f.reduce(function (acc, item) { return acc + ' ' + item }, '')
          } catch (e) {}
        }

        self.updateState(file, 'error', 100, extra)
      }

      self.processNextQueueItem()
    }

    xhr.onerror = function () {
      console.error('Network error while uploading ' + file.name)

      self.updateState(file, 'error', 100, 'There was an issue uploading the file.')
      self.processNextQueueItem()
    }

    xhr.upload.onprogress = function (e) {
      if (e.lengthComputable) {
        self.updateProgress(file, Math.round((e.loaded / e.total) * 100))
      }
    }

    var data = new FormData()

    this.contentType && data.append('content_type', this.contentType)
    this.taxonomy && data.append('taxonomy', this.taxonomy)
    this.public && data.append('public', this.public)
    data.append('object_id', this.objectId)
    data.append('f', file)

    xhr.open('POST', this.uploadUrl)

    if (this.headers) {
      Object.keys(this.headers).forEach(function (header) {
        xhr.setRequestHeader(header, self.headers[header])
      })
    }

    xhr.send(data)
  }

  /////////////////////////////////////////////////////////////////////////////

  // Bootstrap any file uploaders

  function documentReady () {
    return (document.readyState === 'interactive' || document.readyState === 'complete')
  }

  function bootstrap () {
    document.removeEventListener('readystatechange', bootstrap)

    var csrfToken = null

    if (document.querySelector('[name=csrfmiddlewaretoken]')) {
      csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    }

    var fileInputs = document.querySelectorAll('input[type="file"]')

    for (var i = 0; i < fileInputs.length; i++) {
      new FileUploader(fileInputs[i], { 'X-CSRFToken': csrfToken })
    }
  }

  if (documentReady()) {
    bootstrap()
  } else {
    document.addEventListener('readystatechange', bootstrap)
  }
}())
