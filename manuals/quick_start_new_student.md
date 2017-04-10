# Quick-Start-Manual for new Students

## ROS

Die wichtigste Anlaufstelle für Fragen, welche irgendwie mit ROS zutun haben, ist das [ROS-Wiki](http://wiki.ros.org).
Bitte darauf achten, dass sich die Tutorials / Anleitungen auf unsere Version bezieht. 
Eingesetzt wird aktuell das Betriebssystem **Ubuntu 16.04 LTS (Xenial)** mit **ROS Kinetic Kame** und dem Build-System **catkin**.

Übersicht der Links zum schnellen Zugriff:

* [ROS-Wiki](http://wiki.ros.org) - *Erste Anlaufstelle für Informationen bzgl. ROS*
* [Installationsanleitung unter Ubuntu](http://wiki.ros.org/kinetic/Installation/Ubuntu)
  * [Environment Variables](http://wiki.ros.org/ROS/EnvironmentVariables#ROS_MASTER_URI) - *Hier ist auch die ``ROS_MASTER_URI`` zu finden*
  * [Network-Setup](http://wiki.ros.org/ROS/NetworkSetup#Setting_a_name_explicitly) - *Insbesondere die Einträge in der Hosts-Datei*
* [VirtualBox](https://www.virtualbox.org/) - *Software zur Virtualisierung von Betriebssystemen*
* [Introduction](http://wiki.ros.org/ROS/Introduction)
  * [Concepts](http://wiki.ros.org/ROS/Concepts)
  * [Nodes](http://wiki.ros.org/Nodes)
  * [Topic](http://wiki.ros.org/Topics)
  * [Nachrichtentyp](http://wiki.ros.org/msg)
  * [standardmäßige Datentypen](http://wiki.ros.org/ROS/Higher-Level%20Concepts#Message_Ontology) - *``common_msgs`` stack*
  * [Packages](http://wiki.ros.org/Packages)
  * [Bag-File](http://wiki.ros.org/Bags) - *Aufnahmetool*
  * [RQT](http://wiki.ros.org/rqt) - *Plugin-Framework mit hilfreichen Plugins*
  * [RViz](http://wiki.ros.org/rviz) - *Visualisierung*
* [Tutorials](http://wiki.ros.org/ROS/Tutorials)


### Installation 

Eine [ROS Installation für Ubuntu](http://wiki.ros.org/kinetic/Installation/Ubuntu) existiert auf dem Roboter bereits. 
Für arbeiten am eigenen Laptop kann allerdings eine eigene Umgebung aufgesetzt werden. 
Anstelle einer nativen Installation kann dies auch in einer virtuellen Umgebung geschehen.
Hierfür kann man die Virtualisierungsumgebung [VirtualBox](https://www.virtualbox.org/) verwenden, wodurch sich Ubuntu wie ein art "Programm" starten lässt. 
Für die Installation von ROS ist die Variante "**Desktop-Full Install**" zu empfehlen.

Soll die eigene Umgebung mit dem Roboter kommunizieren sind im Wesentlichen zwei Dinge notwendig:

1. Der Rechner, welcher als Master fungiert muss bekannt sein. Dies lässt sich mit dem Setzen einer [Umgebungsvariable](http://wiki.ros.org/ROS/EnvironmentVariables#ROS_MASTER_URI) bewerkstelligen. Anstelle einer IP-Adresse, wird allerdings der "Name des Rechners" angegeben.
2. Der logische Name muss sich zu einer IP-Adresse auflösen lassen. Dies geschieht nicht automatisch. Hierfür muss der [Name explizit](http://wiki.ros.org/ROS/NetworkSetup#Setting_a_name_explicitly) gesetzt werden. Hierfür wird am besten ein Eintrag (Punkt 2.3) in der "hosts" datei (z.B. ``/etc/hosts``) hinzugefügt. **Wichtig:** Da sich beide Rechner finden müssen, muss man den **Eintrag auf beiden Rechner hinzufügen**. 

### Informeller Einstig in ROS

Was ROS ist und welche Ziele verfolgt werden, ist in der [Einführung](http://wiki.ros.org/ROS/Introduction) festgehalten. 
Weiterführend werden auch die entsprechenden [Konzepte](http://wiki.ros.org/ROS/Concepts) von ROS beschrieben. 
Da dies doch recht technisch formuliert ist und sehr viele neue Informationen enthält, hier ein kurzer Einstieg.

Ein Roboter(-System) besteht aus mehren Funktionalitäten. 
Diese Funktionalitäten werden in eigenständigen Programmen abgebildet.
In ROS werden solche Programme als "[Nodes](http://wiki.ros.org/Nodes)" bezeichnet und besitzen einen eigenen Namen.
Nodes werden in [Packages](http://wiki.ros.org/Packages) zusammengefasst, welche eine Organisationseinheit darstellen.
Sollen mehrere Nodes miteinander kommunizieren, geschieht dies über einen Austausch von Nachrichten.
Die Nachrichten haben dabei einen speziellen [Nachrichtentyp](http://wiki.ros.org/msg), wie z.B. Boolean, Integer, String, etc. bei einfachen Nachrichtentypen.
ROS unterstützt bereits [standardmäßig Datentypen](http://wiki.ros.org/ROS/Higher-Level%20Concepts#Message_Ontology) welche für Roboter-Systeme häufig benötigt werden.
Der Austausch von Nachrichten findet über Nachrichtenkanäle statt, welche ebenfalls einen eigenen Namen besitzen.
Solche Kanäle werden in ROS als "[Topic](http://wiki.ros.org/Topics)" bezeichnet.
Dieses Kommunikationsmodell wird auch "[publish / subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)" bezeichnet.
Alleine hierdurch ist es schon möglich, Informationen zwischen zwei Nodes auszutauschen, auch wenn diese sich auf unterschiedlichen Rechnern befinden. 
Das tatsächliche Übertragen und Empfangen der Daten wird dabei von ROS abgenommen und im Betrieb durch den ROS-[Master](http://wiki.ros.org/Master) gesteuert.

Mit den eben beschriebenen Mechanismen sollten sich die meisten Probleme lösen bzw. Funktionalitäten umsetzen lassen.
Darüber hinaus sind in ROS mehrere Werkzeuge verfügbar, welche die Arbeit unterstützen. 
So können online mit dem Programm ``rosbag`` Daten der Topics als [Bag-File](http://wiki.ros.org/Bags) aufgezeichnet und später wieder offline abgespielt werden.
Mit [RQT](http://wiki.ros.org/rqt) stehen viele Plugins (anzeigen der Topics sowie Nachrichten, plotten von Werten, etc.) als GUI zur Verfügung.
Und Visualisierungen (Karten, Punktewolken, Robotermodelle, ...) erhält man mit [RViz](http://wiki.ros.org/rviz).


### Hands-On aka Anfang mit Tutorials

Wer zum ersten mal mit ROS in Berührung kommt und noch immer verwirrt ist macht nichts falsch, das ist normal!
Genau hierfür gibt es eine vielzahl von [Tutorials](http://wiki.ros.org/ROS/Tutorials) welche einen Schritt für Schritt an die arbeit mit ROS heranführen.
Die nachstehende Auswahl gilt als Empfehlung für den Einsteig.


#### Beginner Level

1. [Installing and Configuring Your ROS Environment](http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment)
2. [Navigating the ROS Filesystem](http://wiki.ros.org/ROS/Tutorials/NavigatingTheFilesystem)
3. [Creating a ROS Package](http://wiki.ros.org/ROS/Tutorials/CreatingPackage)
4. [Building a ROS Package](http://wiki.ros.org/ROS/Tutorials/BuildingPackages)
5. [Understanding ROS Nodes](http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes)
6. [Understanding ROS Topics](http://wiki.ros.org/ROS/Tutorials/UnderstandingTopics)
8. [Using rqt_console and roslaunch](http://wiki.ros.org/ROS/Tutorials/UsingRqtconsoleRoslaunch)
11. [Writing a Simple Publisher and Subscriber (C++)](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28c%2B%2B%29)
12. [Writing a Simple Publisher and Subscriber (Python)](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)
13. [Examining the Simple Publisher and Subscriber](http://wiki.ros.org/ROS/Tutorials/ExaminingPublisherSubscriber)
17. [Recording and playing back data](http://wiki.ros.org/ROS/Tutorials/Recording%20and%20playing%20back%20data)
19. [Navigating the ROS wiki](http://wiki.ros.org/ROS/Tutorials/NavigatingTheWiki)


#### Intermediate Level

4. [Running ROS across multiple machines](http://wiki.ros.org/ROS/Tutorials/MultipleMachines)

#### Build-System

* [Catkin Tutorials](http://wiki.ros.org/catkin/Tutorials)
  4. [Overlaying with catkin workspaces](http://wiki.ros.org/catkin/Tutorials/workspace_overlaying)







