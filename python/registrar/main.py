import utils
import funcs as registry_funcs


def main():
    sheet = '1ojoTS8c3RnSsY8UNqo_KFj-XddaxsHB_cw5TRMt4Tac'
    class_slots = utils.get_class_slots(sheet)
    class_preferences = utils.get_class_preferences(sheet)
    print('got data')
    print('number of kids:', len(class_preferences))
    class_assignments = registry_funcs.tough_customer(
        class_preferences,
        class_slots)
    print('placed kids: ', len(class_assignments))
    condition = utils.validate_slots(class_assignments, class_slots) is True
    if condition:
        utils.write_state(sheet, class_assignments)
        print('wrote back to db')
    else:
        print('Slotting Error - debug your damned code')
    return condition == utils.validate_slots(class_assignments, class_slots)


if __name__ == '__main__':
    print(main())
