# 2017-06-22 Meeting Notes

## Discussion Points

### Implementing our own diagram software

It is possible that it might make sense to roll our own diagram instead of utilizing third-party software.
We will already be generating the XML (in the XMI format) for the UML diagrams. Creating the software to
process the diagram, while being more work, would certainly be doable and would give us greater flexibility.

The concept of a primarily aggregation/inheritance diagram was also discussed. In this type of diagram,
the focus would either be on aggregations or inheritance relationships. The other relationships would only be annotated.
Having a diagram like this could be useful to make a large class diagram more comprehensible.

#### Action Items

* Search for anyone with a focus on aggregation and inheritance secondary

### Prexel plugin usage

The actions that occur when pressing a button our using a keyboard shortcut on a
easy-entry string:

* Convert easy-entry into a XML representation of the fragment
* Use XML fragment to generate pretty-printed version of the diagram
* Create entire XML version of UML for entire project
* Create an ASCII version of UML and save to file

### Use prexel as term project

It might make sense to use prexel as the term project for METCS 622. The only downside to this
is that it would probably take longer to develop the Eclipse version of the plugin than for something like
sublime text. Eclipse plugins require using the Eclipse SDK, which has a significantly steeper learning
curve than Sublime text

#### Action Item

* Implement prexel first as a Sublime text plugin and then move onto to a Eclipse Plugin
