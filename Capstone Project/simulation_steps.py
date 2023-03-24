import settings
import simulation_window


def set_target(index, organisms, speed_factors):
    """Step 1 of turn order.
    Check proximity and set new destination when old destination reached."""
    # check if within range of target
    if organisms[index].proximity_check(settings.general["proximity"]):
        organisms[index].set_dest(organisms, speed_factors.get_fast_forward())


def move(index, organisms, speed_factors):
    """Step 2 of turn order.
    Animate movement of the Organism at the given index."""
    # update position, clear shape, move turtle, and redraw shape at new location
    organisms[index].update_pos(settings.screen_size, speed_factors.get_slow_factor())
    organisms[index].clear()
    organisms[index].move()
    organisms[index].draw_dot(settings.general["diameter"])


def battle(index, organisms, speed_factors):
    """Step 3 of turn order.
    Organisms battle each other according to battle method."""
    organisms[index].battle(organisms, speed_factors.get_fast_forward())


def conclude_turn(index, organisms, session_stats, screen, speed_factors):
    """Step 4 of turn order.
    Clear dead organisms and reproduce."""
    organisms[index].increment_age(speed_factors.get_fast_forward())
    # remove an organism from the board if it reaches 0 health
    if organisms[index].is_dead():
        # clear organism animation and remove from list
        organisms[index].clear()
        session_stats.remove_organism(organisms[index].get_attributes())
        organisms.pop(index)
        return False
    # otherwise reproduce offspring when fertile
    else:
        if organisms[index].is_fertile(speed_factors.get_fast_forward(), session_stats.get_prey_pop()):
            identifier = organisms[index].get_identifier()
            pos = organisms[index].get_offspring_pos()
            dest = simulation_window.rand_coords()
            simulation_window.create_organism(organisms,
                                              screen,
                                              identifier,
                                              pos,
                                              dest,
                                              organisms[index].get_attributes(), session_stats)

            # increment generation statistics as needed
            child_gen = organisms[len(organisms) - 1].get_generation()
            if child_gen > session_stats.get_generation(identifier):
                session_stats.set_generation(identifier, child_gen)

        return True
