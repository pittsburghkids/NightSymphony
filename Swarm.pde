public class Swarm {

  ArrayList<Insect> insects;
  int activeCount = 0;

  Swarm() {

    insects = new ArrayList<Insect>();

    insects.add( new Insect(22, "bee.wav") );
    insects.add( new Insect(23, "cicada.wav") );
    insects.add( new Insect(24, "cricket.wav") );
    insects.add( new Insect(25, "mantis.wav") );
    insects.add( new Insect(26, "mosquito.wav") );
    insects.add( new Insect(27, "spittle.wav") );

    insects.add( new Insect(28, "bee.wav") );
    insects.add( new Insect(29, "cicada.wav") );
    insects.add( new Insect(30, "cricket.wav") );
    insects.add( new Insect(31, "mantis.wav") );
    insects.add( new Insect(32, "mosquito.wav") );
    insects.add( new Insect(33, "spittle.wav") );

    insects.add( new Insect(34, "bee.wav") );
    insects.add( new Insect(35, "cicada.wav") );
    insects.add( new Insect(36, "cricket.wav") );
    insects.add( new Insect(37, "mantis.wav") );
    insects.add( new Insect(38, "mosquito.wav") );
    insects.add( new Insect(39, "spittle.wav") );

    insects.add( new Insect(40, "bee.wav") );
    insects.add( new Insect(41, "cicada.wav") );
    insects.add( new Insect(42, "cricket.wav") );
    insects.add( new Insect(43, "mantis.wav") );
    insects.add( new Insect(44, "mosquito.wav") );
    insects.add( new Insect(45, "spittle.wav") );
  }

  int insectCount() {
    return insects.size();
  }

  Insect getInsect(int index) {
    return insects.get(index);
  }

  void toggleInsect(int index) {
    if (!insects.get(index).awake) {
      wakeInsect(index);
    } else {
      sleepInsect(index);
    }
  }

  void wakeInsect(int index) {
    // Start the clock if it isn't ticking
    if (!clock.ticking) clock.start();

    float offset = clock.getPosition();
    insects.get(index).play(offset);
    activeCount++;
  }

  void sleepInsect(int index) {
    insects.get(index).stop();
    activeCount--;
  }

  void trigger() {
    for (int i = 0; i < insects.size (); i++) {
      if (insects.get(i).awake) insects.get(i).trigger();
    }
  }
}

