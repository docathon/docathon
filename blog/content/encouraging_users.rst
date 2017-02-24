Encouraging user help for the Docathon (and beyond)
###################################################

:date: 2017-02-24
:modified: 2017-02-24
:tags: communication, coding
:category: info
:slug: encouraging-user-docathon
:authors: Chris Holdgraf, Nelle Varoquaux
:summary: Tips and tricks to encourage users to contribute documentation!

Documentation is a great way to get new users and contributors involved in
your project. It requires less knowledge of the intricacies of your codebase,
and can be both fun and easily appreciated by others.

However, it’s not always clear to people how to contribute documentation. At
the Docathon there will be many attendees who have experience in coding, but
aren’t sure where to begin. This is a great opportunity to get some work done
and to grow your community.

A commonly-forgotten part of project documentation is information about how
users can become developers. Each project has its idiosyncrasies and preferred
contribution workflow, and this isn’t always obvious to people. We recommend
the following steps:

  - **Think about your contribution workflow.** Do you have one? If not, then
    spend some time thinking about how you’d like contributions to occur. If
    anything else, it is helpful to explicitly state that you welcome
    contributions in the form of pull requests.
  - **Make it clear how your documentation is organized.** It’s good to have
    documentation split up by the scope of its content. E.g., don’t intermingle
    high-level tutorials with examples showing off a specific piece of the API.
  - **Make it obvious what kinds of documentation goes where.** It will help
    new contributors, and make it easier for new users to use your project.
  - **Create a “documentation” label, as well as a “new-contributor-friendly”
    label** for your repository. Come up with some ways in which you’d like
    your documentation to improve (e.g., ``#32: write an example for the
    statistics module``, or ``make docstrings numpydoc compatible``) and tag it
    with these labels. Along these lines, make your tickets as descriptive,
    clear, and actionable as you can. “Add references to the ``linear_model``
    function” is better than “Improve documentation for the ``linear_model``
    function”.
  - **Make sure that your project has at least one or two examples** that can
    be highlighted as “good” forms of documentation. Many users will riff off
    of what is already there, so if you can say “you should make your example
    similar in style and scope to XXX”, it will help them.
  - **Write a short “how to contribute” guide.** You might link to a guide on
    opening pull-requests in github, then explain if you have any information
    you’d like to see in the pull request.
  - **Finally, don’t be too nitpicky about the PRs that new users make**, and
    make sure to be friendly to new contributors! Documentation (usually)
    won’t break anything, so don’t let good become an enemy of perfect! Is the
    pull request an improvement? Just press the green button.

Remember - documentation is the first point of contact that most people have
with your package, so it’s worth putting in time to make it as clear,
complete, and maintainable as possible! 
