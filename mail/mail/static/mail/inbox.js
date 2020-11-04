document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#compose-heading').innerHTML = `<h3>New Email</h3>`;

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the mailbox's content
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // goes through each email 
    emails.forEach(element => {
      // creates a div for each email and adds a class name email
      const email = document.createElement('div');
      email.className += "email";
  
      // adds a grey background to read emails
      if (element.read){
        email.className += " email-read";
      }
  
      // creates a paragraph element for the sender and add that info
      const sender = document.createElement('p');
      sender.innerHTML = "<b>" + element.sender + "</b>";
  
      // creates a paragraph element for the subject and add that info
      const subject = document.createElement('p');
      subject.innerHTML = element.subject;
  
      // creates a paragraph element for the timestamp and add that info
      const timestamp = document.createElement('p');
      timestamp.innerHTML = element.timestamp;

      // Adds the event listiner the click
      email.addEventListener('click', () => see_email(element.id, mailbox));
  
      // adds all elements to the current emaildiv
      email.append(sender, subject, timestamp);
  
      // append to the emails-views id
      document.querySelector('#emails-view').append(email);
    });
 });
}

function send_mail() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  return false;
}

function see_email(id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email.body);
    // Creates a div to receive the content and add a class name
    const mail = document.createElement('div');
    mail.className = "email-view";
    
    // Container for the sender
    const sender = document.createElement('p');
    sender.innerHTML = "<b>Sender:</b> " + email.sender;
    
    // Container for the recipients
    const recipients = document.createElement('p');
    recipients.innerHTML = "<b>Recipients:</b> " + email.recipients;
    
    // Container for the subject
    const subject = document.createElement('p');
    subject.innerHTML = "<b>Subject:</b> " + email.subject;

    // Container for the timestamp
    const timestamp = document.createElement('p');
    timestamp.innerHTML = "<b>Sent:</b> " + email.timestamp;

    // Div for the info above
    const info = document.createElement('div');
    info.id = "info-field";
    info.append(sender, recipients, subject, timestamp);
    
    // Container for the body of the email
    const body = document.createElement('textarea');
    body.id = "body-field";
    body.readOnly = true;
    body.innerHTML = email.body;

    if (mailbox !== 'sent'){
      // creates the buttons for reply and archive
      const replyBtn = document.createElement('button');
      replyBtn.innerHTML = "Reply";
      replyBtn.className += "btn btn-outline-primary";
      const archiveBtn = document.createElement('button');
      archiveBtn.className += "btn btn-outline-secondary";
      // checks the mailbox for proper archiving behavior
      if (mailbox === 'archive'){
        archiveBtn.innerHTML = "Unarchive";
      } else {
        archiveBtn.innerHTML = "Archive";
      }
      
      // Adds the proper functionality to the buttons
      replyBtn.addEventListener('click', () => reply(email.id));
      archiveBtn.addEventListener('click', () => archive(email.id, mailbox));

      // Adds to the div that recieves all the email info
      mail.append(replyBtn, archiveBtn, info, body);
    } else {
      mail.append(info, body);
    }
    
    // Clears the id's content and adds the email info
    document.querySelector("#emails-view").innerHTML = "";
    document.querySelector("#emails-view").append(mail);
  })

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function reply(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Reply to info
    document.querySelector('#compose-heading').innerHTML = `<h3>Reply to ${email.sender}</h3>`;

    // Adds the proper values to the correct fields
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.slice(0, 3) === 'Re:'){
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = "Re: " + email.subject;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n` + email.body;
  });
}

function archive(id, mailbox){
  if (mailbox === 'archive'){
    fetch(`/emails/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: false
      })
    })
  } else {
      fetch(`/emails/${id}`, {
        method: "PUT",
        body: JSON.stringify({
          archived: true
        })
      })
  }
  // loads the inbox
  load_mailbox('inbox');
}