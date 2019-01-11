import sys
import unittest
from app import app
import setupdb
import setuptestdb
from controller.database import db
from controller.database_controller import database_controller
from model.skill_model import SkillModel
from model.milestone_model import MilestoneModel
from model.database_model import Date, Skill, Users, Association, MilestoneAssociation, Hierarchy, Guidelines


def setUpModule():
    app.testing = True

class testDatabaseController(unittest.TestCase):

    def setUp(self):

        self.valdemar = Users(username='Valdemar-Forsberg', name="Valdemar Forsberg")
        self.karl = Users(username='Karl-Kalagin', name="Karl Kalagin")
        self.isaac = Users(username='Isaac-Hunt', name="Isaac Hunt")

        db.session.add(self.valdemar)
        db.session.add(self.karl)
        db.session.add(self.isaac)

        self.prog = Skill(name='Programming', path='Programming', root=True)
        self.java1 = Skill(name='Java', path='Programming/Java')
        self.python1 = Skill(name='Python', path='Programming/Python')
        self.js1 = Skill(name='JavaScript', path='Programming/Javascript')

        db.session.add(self.java1)
        db.session.add(self.python1)
        db.session.add(self.prog)
        db.session.add(self.js1)
        

        self.date1 = Date()
        db.session.add(self.date1)
        self.a = Association(level=4)
        self.a.skill_assoc = self.js1
        self.a.date_assoc = self.date1
        self.a.users_assoc = self.isaac


        self.b = MilestoneAssociation(comment='bootcamp', level=4)
        self.b.skill_milestone_assoc = self.js1
        self.b.date_milestone_assoc = self.date1
        self.b.users_milestone_assoc = self.isaac
        db.session.add(self.b)


        self.a1 = Association(level=3)
        self.a1.skill_assoc = self.js1
        self.a1.date_assoc = self.date1
        self.a1.users_assoc = self.isaac
        db.session.add(self.a1)

        self.a3 = Association(level=3)
        self.a3.skill_assoc = self.java1
        self.a3.date_assoc = self.date1
        self.a3.users_assoc = self.valdemar
        db.session.add(self.a3)


        self.a4 = Association(level=3)
        self.a4.skill_assoc = self.js1
        self.a4.date_assoc = self.date1
        self.a4.users_assoc = self.karl
        db.session.add(self.a4)


        self.a5 = Association(level=4)
        self.a5.skill_assoc = self.python1
        self.a5.date_assoc = self.date1
        self.a5.users_assoc = self.valdemar
        db.session.add(self.a5)

        self.a6 = Association(level=2)
        self.a6.skill_assoc = self.java1
        self.a6.date_assoc = self.date1
        self.a6.users_assoc = self.isaac
        db.session.add(self.a6)


        self.a7 = Association(level=2)
        self.a7.skill_assoc = self.js1
        self.a7.date_assoc = self.date1
        self.a7.users_assoc = self.valdemar
        db.session.add(self.a7)


        self.a8 = Association(level=3)
        self.a8.skill_assoc = self.python1
        self.a8.date_assoc = self.date1
        self.a8.users_assoc = self.karl
        db.session.add(self.a8)

        self.a9 = Association(level=3)
        self.a9.skill_assoc = self.python1
        self.a9.date_assoc = self.date1
        self.a9.users_assoc = self.isaac
        db.session.add(self.a9)


        self.a10 = Association(level=1)
        self.a10.skill_assoc = self.java1
        self.a10.date_assoc = self.date1
        self.a10.users_assoc = self.karl
        db.session.add(self.a10)



        self.x = Hierarchy()
        self.x.parent_skill_assoc = self.prog
        self.x.child_skill_assoc = self.js1
        db.session.add(self.x)

        self.x1 = Hierarchy()
        self.x1.parent_skill_assoc = self.prog
        self.x1.child_skill_assoc = self.java1
        db.session.commit()

        self.pythonlevel1 = Guidelines(skill_id=2, level=1, information="gar nicht gut")
        self.pythonlevel2 = Guidelines(skill_id=2, level=2, information="nicht gut")
        self.pythonlevel3 = Guidelines(skill_id=2, level=3, information="mittel")
        self.pythonlevel4 = Guidelines(skill_id=2, level=4, information="schon gut")
        self.pythonlevel5 = Guidelines(skill_id=2, level=5, information="what a man :O")
        db.session.add(self.pythonlevel1)
        db.session.add(self.pythonlevel2)
        db.session.add(self.pythonlevel3)
        db.session.add(self.pythonlevel4)
        db.session.add(self.pythonlevel5)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        db.session.commit()
        setuptestdb.dropdb()

    def test_search_success(self):
        result = database_controller.search({"Java": 1})
        expected_result = dict([self.valdemar, self.karl, self.isaac],[])
        self.assertEquals(result, expected_result)

    def test_search_with_no_results(self):
        result = database_controller.search({"Haskell": 1})
        expected_result = dict([],[])
        self.assertEquals(result, expected_result)

    def test_set_skill(self):
        database_controller.set_skills("Valdemar-Forsberg", {"F#": 2})
        skill_exists = Skill.query.filter_by(Skill.name == "F#").first()
        self.assertIsNotNone(skill_exists)

    def test_add_milestone(self):
        database_controller.add_milestone("Karl-Kalagin", "Programming/Java", "2019-01-01", "testmiltestone", 5)
        #skill_id = Skill.query.filter_by(path=)
        association_exists = MilestoneAssociation.query.filter(MilestoneAssociation.milestone_skill_id == self.java1.id,
                                                               MilestoneAssociation.milestone_users_id == self.karl.id)
        self.assertIsNotNone(association_exists)

    def test_get_milestones(self):
        result = database_controller.get_milestones("Karl-Kalagin", "JavaScript")
        expected_result = [MilestoneModel(self.b.date_milestone_assoc, "bootcamp", self.b.level)]

    def test_get_assocs(self):
        association_exists = database_controller.get_assocs(1,1,1,"first")
        self.assertIsNotNone(association_exists)

    def test_get_all_users(self):
        result = database_controller.get_all_users()
        expected_result = Users.query.all()
        self.assertEquals(result, expected_result)

    def test_get_subcategories(self):
        result = database_controller.get_subcategories("Valdemar-Forsberg", "Java")
        expected_result = ["JavaScript", "Python"]
        self.assertEqual(result, expected_result)

    def test_create_hierachy(self):
        self.flask = Skill(name='Flask')
        db.session.add(self.flask)
        database_controller.create_hierachy('Python', 'Flask')
        hierarchy_exists = Hierarchy.query.filter(Hierarchy.child_skill_assoc == self.flask,
                                       Hierarchy.parent_skill_assoc == self.python1).first()
        self.assertIsNotNone(hierarchy_exists)
        Skill.query.filter_by(id=Skill.query.filter_by(name="Flask").first().id).delete()

    def test_get_path_with_guidlines(self):
        pass


    def test_get_skill(self):
        result = database_controller.get_skill("Python")
        self.assertEqual(result.name, "Python")


    def test_get_user(self):
        result = database_controller.get_user_id("Valdemar-Forsberg")
        self.assertEqual(result.username, "Valdemar-Forsberg")
        self.assertEqual(result.name, "Valdemar Forsberg")

    def test_get_date_from_id(self):
        result = database_controller.get_date_from_id(1)
        self.assertEqual(result, 1)

    def test_get_user_from_id(self):
        result = database_controller.get_user_from_id(1)
        self.assertEqual(result.username, "Valdemar-Forsberg")

    def test_get_skill_from_id(self):
        result = database_controller.get_skill_from_id(1)
        self.assertEqual(result.name, "Java")

    def test_create_skill(self):
        new_skill = Skill(name='C#')
        db.session.add(new_skill)
        db.session.commit()
        self.assertEqual(Skill.query.filter_by(name="C#").first().name, "C#")
        Skill.query.filter_by(id=Skill.query.filter_by(name="C#").first().id).delete()

    def test_exists_success(self):
        self.assertTrue(Users.query.filter_by(username="Valdemar-Forsberg").first())

    def test_exists_fail(self):
        self.assertFalse(Users.query.filter_by(username="Lisza-Zulu").first())

    def test_get_skills(self):
        result = database_controller.get_skills("Valdemar-Forsberg")
        self.assertEqual(result, [[["Java", 3,[]]],["Python",4,[]],["JavaScript",2,[]]])

    def test_get_skills_inexistent(self):
        result = database_controller.get_skills("Lisza-Zulu")
        self.assertIsNone(result)

    def test_get_guideline_dict(self):
        pass

    def test_get_guideline_dict(self):
        pass

    def test_change_guidlelines(self):
        pass

    def test_get_guideline_dict(self):
        pass



    def test_create_user(self):
        database_controller.create_user("Lisza-Zulu", "Lisza Zulu")
        self.assertEqual(Users.query.filter_by(name="Lisza Zulu").first().name(), "Lisza Zulu")

    def test_get_recent_level(self):
        result = database_controller.get_recent_level(1,1)
        self.assertEqual(result, 3)

    def test_get_profile_models(self):
        result = database_controller.get_profile_models([self.valdemar])
        expected_result = [dict(username='Valdemar-Forsberg',
                                name='Valdemar Forsberg',
                                skills=[[["Java", 3,[]]],
                                        ["Python",4,[]],
                                        ["JavaScript",2,[]]]
                                )]
        self.assertEqual(result, expected_result)

    def test_sum_relevant_skills(self):
        result = database_controller.sum_relevant_skills(dict(username='Valdemar-Forsberg',
                                                              name='Valdemar Forsberg',
                                                              skills=[[["Java", 3,[]]],
                                                                      ["Python",4,[]],
                                                                      ["JavaScript",2,[]]]
                                                              ),
                                                              ["Java","JavaScript"])

        expected_result = 5
        self.assertEqual(result, expected_result)

    def test_build_subcategories(self):
        result = database_controller.build_subcategories('Valdemar-Forsberg', "Java")
        expected_result = SkillModel("Java", 3, [SkillModel('JavaScript', 2)])
        self.assertEquals(result, expected_result)

    def test_remove_skill_from_database(self):
        pass

    def test_remove_skill(selfself):
        pass

    def test_remove_milestone(self):
        pass


