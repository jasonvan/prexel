# 2017-06-08 Meeting Notes

## Priority 1:

We needed to determine some code that would be suitable for adding Prexel notation to that people could review and perhaps take a
quiz on.

### Ideas:
* Java Tutorials
* Gang of Four - Java source code (e.g., Abstract Factory)

## Priority 2:

Review entry syntax for how a user might use Prexel. Needs to be quick to type and intuitive.

## IDE Plugin Description:

The tool would probably be some sort of plugin that is used inside of an IDE. As the user types they could add prexel annotations, that with a push of a button would expand to into pretty-printed UML. The tool would also need to generate XML ( or maybe xmi ) for each of the fragments. These fragments would then be combined into one XML document that could be used with a third-party UML design tool

## Questions:

* Should we generate XML or something else?
* Seems like this might be two parts. The IDE itegration, the handles the pretty-printing and syntax highlighting and the processing
of the UML fragments. 
* Perhaps pretty-printing should be separate so the processing of the fragments is not contigent on 
the pretty-printing features